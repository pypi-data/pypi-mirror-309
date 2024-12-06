# Copyright (c) 2024 Moritz E. Beber
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.


"""Provide the knowledge chat application."""

from datetime import timedelta
from time import perf_counter
from uuid import UUID

import structlog
from eventsourcing.application import AggregateNotFoundError, Application
from eventsourcing.persistence import Recording
from eventsourcing.utils import EnvType
from langchain_community.graphs import Neo4jGraph
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tracers.base import BaseTracer

from knowledge_chat.application import (
    AbstractKnowledgeChat,
    ConversationDTO,
    ExchangeOutputDTO,
    UserDTO,
)
from knowledge_chat.domain.error import NotFoundError
from knowledge_chat.domain.model import Conversation, Query, User
from knowledge_chat.domain.service import DomainServiceRegistry
from knowledge_chat.infrastructure.settings.agent_settings import AgentSettings


logger = structlog.get_logger(__name__)


class KnowledgeChat(Application, AbstractKnowledgeChat):
    """Define the knowledge chat application."""

    def __init__(
        self,
        *,
        domain_service_registry: DomainServiceRegistry,
        knowledge_graph: Neo4jGraph,
        chat_model: BaseChatModel,
        agent_settings: AgentSettings,
        env: EnvType | None = None,
        **kwargs,
    ) -> None:
        super().__init__(env=env, **kwargs)
        self.domain_service_registry = domain_service_registry
        self.knowledge_graph = knowledge_graph
        self.chat_model = chat_model
        self.agent_settings = agent_settings

    def create_user(self, user: UserDTO) -> UUID:
        """Create a new user instance and persist it."""
        try:
            domain_user = self._get_user(user_id=user.user_id)
            logger.error("User already exists.", user=user)
        except NotFoundError:
            domain_user = user.create()
            self.save(domain_user)
        return domain_user.id

    def _get_user(self, user_id: str) -> User:
        """Get a user's state by their identifier."""
        uuid = User.create_id(user_id=user_id)
        try:
            result: User = self.repository.get(uuid)
        except AggregateNotFoundError as error:
            raise NotFoundError(uuid=uuid) from error

        return result

    def get_user(self, user_id: str) -> UserDTO:
        """Get user data by their identifier."""
        user = self._get_user(user_id=user_id)
        return UserDTO.from_user(user=user)

    def start_conversation(self, user_id: str) -> UUID:
        """Add a new conversation to the user."""
        user = self._get_user(user_id)
        conversation = Conversation(user_reference=user.id)
        user.add_conversation(conversation_reference=conversation.id)
        self.save(user, conversation)
        return conversation.id

    def _get_conversation(self, conversation_id: UUID) -> Conversation:
        """Get a conversation's state by its identifier."""
        try:
            result: Conversation = self.repository.get(conversation_id)
        except AggregateNotFoundError as error:
            raise NotFoundError(uuid=conversation_id) from error

        return result

    def get_conversation(self, conversation_id: UUID) -> ConversationDTO:
        """Get conversation data by its identifier."""
        conversation = self._get_conversation(conversation_id)
        return ConversationDTO.from_conversation(conversation=conversation)

    def respond_to(
        self,
        query: str,
        conversation_id: UUID,
        callbacks: list[BaseTracer] | None = None,
    ) -> ExchangeOutputDTO:
        """Use a configured agent to respond to the given query."""
        conversation = self._get_conversation(conversation_id)
        logger.debug("CONVERSATION_RESTORED")

        conversation.raise_query(Query(text=query))

        start = perf_counter()
        agent = self.domain_service_registry.get_response_agent(
            self.agent_settings,
            self.knowledge_graph,
            self.chat_model,
        )
        logger.debug(
            "AGENT_CREATED",
            duration=timedelta(seconds=perf_counter() - start),
        )

        start = perf_counter()
        agent.generate_response(conversation, callbacks=callbacks)
        logger.debug(
            "RESPONSE_GENERATED",
            duration=timedelta(seconds=perf_counter() - start),
        )
        self.save(conversation)
        assert conversation.latest_exchange is not None  # noqa: S101
        return ExchangeOutputDTO.from_exchange(conversation.latest_exchange)

    def _notify(self, recordings: list[Recording]) -> None:
        super()._notify(recordings)
        for recording in recordings:
            logger.debug("EVENT_RECORDED", recording=recording.domain_event)
