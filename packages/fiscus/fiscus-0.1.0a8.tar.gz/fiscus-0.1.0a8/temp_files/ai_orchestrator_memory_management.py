import os
import pickle
import logging
from typing import Any, Callable, Optional, Dict, List
from enum import Enum
from .enums import (
    FiscusMemoryRetrievalType,
    FiscusMemoryStorageType,
)
from .response import FiscusError, FiscusErrorCode

# Define directories for different storage types
PICKLE_STORAGE_DIR = 'pickle_storage'
LOCAL_STORAGE_DIR = 'local_storage'

class StorageType(Enum):
    LOCAL = 'local'
    PICKLE = 'pickle'
    IN_MEMORY = 'in_memory'  # For short-term memory
    DATABASE = 'database'    # Placeholder for future expansion

class Memory:
    """
    Default Memory class that handles in-memory, local, and pickle storage.
    """
    def __init__(self, storage_type: str, embedding_model: Optional[Any], indexing_algorithm: Optional[str], logger: logging.Logger):
        self.storage_type = storage_type
        self.embedding_model = embedding_model
        self.indexing_algorithm = indexing_algorithm
        self.logger = logger
        self.short_term_memory = []
        self.long_term_memory = []
        self.in_memory_state = {}
        # Placeholder for database connections
        self.database = {}

    def semantic_search(self, query, top_k, embedding_model, indexing_algorithm, is_short_term, **kwargs):
        # Implement semantic search logic
        self.logger.debug("Performing semantic search.")
        memory = self.short_term_memory if is_short_term else self.long_term_memory
        # For simplicity, return the last `top_k` entries
        return '\n'.join(memory[-top_k:])

    def keyword_search(self, query, is_short_term, **kwargs):
        # Implement keyword search logic
        self.logger.debug("Performing keyword search.")
        memory = self.short_term_memory if is_short_term else self.long_term_memory
        # For simplicity, return entries containing the query
        results = [entry for entry in memory if query in entry]
        return '\n'.join(results)

    def hybrid_search(self, query, top_k, similarity_threshold, embedding_model, indexing_algorithm, is_short_term, **kwargs):
        # Implement hybrid search logic
        self.logger.debug("Performing hybrid search.")
        # For simplicity, combine semantic and keyword search results
        semantic_results = self.semantic_search(query, top_k, embedding_model, indexing_algorithm, is_short_term, **kwargs)
        keyword_results = self.keyword_search(query, is_short_term, **kwargs)
        return '\n'.join(set(semantic_results.split('\n') + keyword_results.split('\n')))

    def store(self, data, embedding_model, indexing_algorithm, is_short_term, **kwargs):
        self.logger.debug("Storing data in memory.")
        if is_short_term:
            self.short_term_memory.append(data)
        else:
            self.long_term_memory.append(data)

    def update(self, data, update_condition, embedding_model, indexing_algorithm, is_short_term, **kwargs):
        self.logger.debug("Updating data in memory.")
        memory = self.short_term_memory if is_short_term else self.long_term_memory
        for idx, entry in enumerate(memory):
            if update_condition(entry):
                memory[idx] = data
                break

    def upsert(self, data, embedding_model, indexing_algorithm, is_short_term, **kwargs):
        self.logger.debug("Upserting data in memory.")
        update_condition = kwargs.get('update_condition')
        if update_condition:
            self.update(data, update_condition, embedding_model, indexing_algorithm, is_short_term, **kwargs)
        else:
            self.store(data, embedding_model, indexing_algorithm, is_short_term, **kwargs)

class _AIOrchestratorMemoryManagementMixin:
    """
    Mixin class for AI Orchestrator memory management.
    Provides methods to store and retrieve memory, both stateful and stateless,
    supporting various storage and retrieval strategies.
    """

    MAX_TOKEN_LIMIT = 1000  # Maximum token limit for retrieved context

    def retrieve_memory(
        self,
        input_text: str,
        retrieval_strategy: Optional[FiscusMemoryRetrievalType] = None,
        state_id: Optional[str] = None,
        context: Optional[str] = None,
        top_k: int = 5,
        similarity_threshold: float = 0.8,
        retrieval_callback: Optional[Callable[[str], Optional[str]]] = None,
        storage_type: str = 'local',
        is_short_term: bool = True,
        **kwargs,
    ) -> str:
        """
        Retrieve memory context relevant to the input, supporting different storage types.
        """
        # Initialize memory if not provided
        if self.memory is None:
            self.logger.debug("Memory is not provided. Initializing default memory.")
            self.memory = Memory(
                storage_type=storage_type,
                embedding_model=self.embedding_model,
                indexing_algorithm=self.indexing_algorithm,
                logger=self.logger
            )

        # Set default retrieval strategy if not provided
        retrieval_strategy = retrieval_strategy or self.retrieval_strategy or FiscusMemoryRetrievalType.SEMANTIC_SEARCH

        # Validate retrieval strategy
        if not isinstance(retrieval_strategy, FiscusMemoryRetrievalType):
            self.logger.error(f"Invalid retrieval strategy: {retrieval_strategy}")
            raise ValueError(f"Invalid retrieval strategy: {retrieval_strategy}")

        # Validate storage type
        if storage_type.lower() not in [st.value for st in StorageType]:
            self.logger.error(f"Invalid storage type: {storage_type}")
            raise ValueError(f"Invalid storage type: {storage_type}")
        storage_type = storage_type.lower()

        # Stateful retrieval
        if state_id:
            self.logger.debug(f"Retrieving stateful memory for state_id: {state_id} with storage type: {storage_type}")
            context = self._retrieve_stateful_memory(state_id, storage_type, retrieval_callback)
            if context:
                context = self._trim_context(context)
                self.audit_trail.record('memory_retrieval', {'input': input_text, 'context': context})
                return context
            else:
                self.logger.warning(f"No context found for state_id {state_id}. Proceeding with stateless retrieval.")

        # Stateless retrieval
        self.logger.debug(f"Retrieving {'short-term' if is_short_term else 'long-term'} memory using strategy: {retrieval_strategy}")
        context = self._retrieve_stateless_memory(
            input_text=input_text,
            retrieval_strategy=retrieval_strategy,
            top_k=top_k,
            similarity_threshold=similarity_threshold,
            is_short_term=is_short_term,
            **kwargs,
        )

        context = self._trim_context(context)
        self.audit_trail.record('memory_retrieval', {'input': input_text, 'context': context})
        return context

    def _retrieve_stateful_memory(
        self,
        state_id: str,
        storage_type: str,
        retrieval_callback: Optional[Callable[[str], Optional[str]]],
    ) -> Optional[str]:
        """
        Retrieve memory based on state_id using specified storage type.
        """
        storage_methods = {
            StorageType.LOCAL.value: self._retrieve_local_state,
            StorageType.PICKLE.value: self._retrieve_pickle_state,
            StorageType.IN_MEMORY.value: self._retrieve_in_memory_state,
            # StorageType.DATABASE.value: self._retrieve_database_state,  # For future use
        }

        context = None
        try:
            context = storage_methods[storage_type](state_id)
            if context:
                self.logger.debug(f"Retrieved stateful memory from {storage_type} storage for state_id: {state_id}")
        except KeyError:
            self.logger.error(f"Unsupported storage type: {storage_type}")
            raise ValueError(f"Unsupported storage type: {storage_type}")
        except Exception as e:
            self.logger.error(f"Error retrieving stateful memory: {e}", exc_info=True)

        # Fallback to retrieval callback
        if not context and retrieval_callback:
            self.logger.debug(f"Attempting retrieval via callback for state_id: {state_id}")
            try:
                context = retrieval_callback(state_id)
                if context:
                    self.logger.debug("Retrieved context via callback.")
            except Exception as e:
                self.logger.error(f"Error in retrieval callback: {e}", exc_info=True)

        return context

    def _retrieve_stateless_memory(
        self,
        input_text: str,
        retrieval_strategy: FiscusMemoryRetrievalType,
        top_k: int,
        similarity_threshold: float,
        is_short_term: bool,
        **kwargs,
    ) -> str:
        """
        Retrieve stateless memory based on the specified strategy.
        """
        retrieval_func = self.memory_retrieval_logic or self._default_memory_retrieval

        try:
            context = retrieval_func(
                query=input_text,
                retrieval_strategy=retrieval_strategy,
                top_k=top_k,
                similarity_threshold=similarity_threshold,
                is_short_term=is_short_term,
                **kwargs,
            )
            return context
        except Exception as e:
            self.logger.error(f"Error in stateless memory retrieval: {e}", exc_info=True)
            return ""

    def _default_memory_retrieval(
        self,
        query: str,
        retrieval_strategy: FiscusMemoryRetrievalType,
        top_k: int,
        similarity_threshold: float,
        is_short_term: bool,
        **kwargs,
    ) -> str:
        """
        Default memory retrieval implementation based on the strategy.
        """
        if retrieval_strategy == FiscusMemoryRetrievalType.SEMANTIC_SEARCH:
            return self.memory.semantic_search(
                query=query,
                top_k=top_k,
                embedding_model=self.embedding_model,
                indexing_algorithm=self.indexing_algorithm,
                is_short_term=is_short_term,
                **kwargs,
            )
        elif retrieval_strategy == FiscusMemoryRetrievalType.KEYWORD_SEARCH:
            return self.memory.keyword_search(query=query, is_short_term=is_short_term, **kwargs)
        elif retrieval_strategy == FiscusMemoryRetrievalType.HYBRID_SEARCH:
            return self.memory.hybrid_search(
                query=query,
                top_k=top_k,
                similarity_threshold=similarity_threshold,
                embedding_model=self.embedding_model,
                indexing_algorithm=self.indexing_algorithm,
                is_short_term=is_short_term,
                **kwargs,
            )
        else:
            self.logger.error(f"Unknown retrieval strategy: {retrieval_strategy}")
            raise ValueError(f"Unknown retrieval strategy: {retrieval_strategy}")

    def store_memory(
        self,
        data: Any,
        storage_strategy: Optional[FiscusMemoryStorageType] = None,
        state_id: Optional[str] = None,
        update_condition: Optional[Callable[[Any], bool]] = None,
        storage_callback: Optional[Callable[[str, Any], None]] = None,
        storage_type: str = 'local',
        is_short_term: bool = True,
        **kwargs,
    ) -> None:
        """
        Store data into memory with options for stateful and stateless storage.
        """
        # Initialize memory if not provided
        if self.memory is None:
            self.logger.debug("Memory is not provided. Initializing default memory.")
            self.memory = Memory(
                storage_type=storage_type,
                embedding_model=self.embedding_model,
                indexing_algorithm=self.indexing_algorithm,
                logger=self.logger
            )

        # Set default storage strategy if not provided
        storage_strategy = storage_strategy or self.storage_strategy or FiscusMemoryStorageType.APPEND

        # Validate storage strategy
        if not isinstance(storage_strategy, FiscusMemoryStorageType):
            self.logger.error(f"Invalid storage strategy: {storage_strategy}")
            raise ValueError(f"Invalid storage strategy: {storage_strategy}")

        # Validate storage type
        if storage_type.lower() not in [st.value for st in StorageType]:
            self.logger.error(f"Invalid storage type: {storage_type}")
            raise ValueError(f"Invalid storage type: {storage_type}")
        storage_type = storage_type.lower()

        # Stateful storage
        if state_id:
            self.logger.debug(f"Storing stateful memory for state_id: {state_id} in {storage_type} storage")
            success = self._store_stateful_memory(state_id, data, storage_type, storage_callback)
            if success:
                self.logger.debug(f"Successfully stored stateful memory for state_id: {state_id}")
                return
            else:
                self.logger.warning(f"Failed to store stateful memory for state_id: {state_id}")

        # Stateless storage
        self.logger.debug(f"Storing {'short-term' if is_short_term else 'long-term'} memory using strategy: {storage_strategy}")
        storage_func = self.memory_storage_logic or self._default_memory_storage

        try:
            storage_func(
                data=data,
                storage_strategy=storage_strategy,
                update_condition=update_condition,
                is_short_term=is_short_term,
                **kwargs,
            )
            self.audit_trail.record('memory_storage', {'data': data})
        except Exception as e:
            self.logger.error(f"Error in stateless memory storage: {e}", exc_info=True)
            raise

    def _store_stateful_memory(
        self,
        state_id: str,
        data: Any,
        storage_type: str,
        storage_callback: Optional[Callable[[str, Any], None]],
    ) -> bool:
        """
        Store stateful memory using the specified storage type.
        """
        storage_methods = {
            StorageType.LOCAL.value: self._store_local_state,
            StorageType.PICKLE.value: self._store_pickle_state,
            StorageType.IN_MEMORY.value: self._store_in_memory_state,
            # StorageType.DATABASE.value: self._store_database_state,  # For future use
        }

        success = False
        try:
            success = storage_methods[storage_type](state_id, data)
            if success:
                self.logger.debug(f"Stored stateful memory in {storage_type} storage for state_id: {state_id}")
        except KeyError:
            self.logger.error(f"Unsupported storage type: {storage_type}")
            raise ValueError(f"Unsupported storage type: {storage_type}")
        except Exception as e:
            self.logger.error(f"Error storing stateful memory: {e}", exc_info=True)

        # Fallback to storage callback
        if not success and storage_callback:
            self.logger.debug(f"Attempting storage via callback for state_id: {state_id}")
            try:
                storage_callback(state_id, data)
                self.logger.debug("Stored stateful memory via callback.")
                success = True
            except Exception as e:
                self.logger.error(f"Error in storage callback: {e}", exc_info=True)

        return success

    def _default_memory_storage(
        self,
        data: Any,
        storage_strategy: FiscusMemoryStorageType,
        update_condition: Optional[Callable[[Any], bool]],
        is_short_term: bool,
        **kwargs,
    ) -> None:
        """
        Default implementation for memory storage strategies.
        """
        if storage_strategy == FiscusMemoryStorageType.APPEND:
            self.memory.store(
                data,
                embedding_model=self.embedding_model,
                indexing_algorithm=self.indexing_algorithm,
                is_short_term=is_short_term,
                **kwargs,
            )
        elif storage_strategy == FiscusMemoryStorageType.UPDATE:
            if not update_condition:
                self.logger.error("An update_condition function must be provided for UPDATE strategy.")
                raise ValueError("An update_condition function must be provided for UPDATE strategy.")
            self.memory.update(
                data,
                update_condition=update_condition,
                embedding_model=self.embedding_model,
                indexing_algorithm=self.indexing_algorithm,
                is_short_term=is_short_term,
                **kwargs,
            )
        elif storage_strategy == FiscusMemoryStorageType.UPSERT:
            self.memory.upsert(
                data,
                embedding_model=self.embedding_model,
                indexing_algorithm=self.indexing_algorithm,
                is_short_term=is_short_term,
                **kwargs,
            )
        else:
            self.logger.error(f"Unknown storage strategy: {storage_strategy}")
            raise ValueError(f"Unknown storage strategy: {storage_strategy}")

    def _trim_context(self, context: str) -> str:
        """
        Trim the context to ensure it doesn't exceed the maximum token limit.
        """
        if len(context) > self.MAX_TOKEN_LIMIT:
            context = context[:self.MAX_TOKEN_LIMIT]
            self.logger.info("Context trimmed to fit within token limit.")
        return context

    # Local storage methods
    def _retrieve_local_state(self, state_id: str) -> Optional[str]:
        """
        Retrieve stateful memory from local storage.
        """
        os.makedirs(LOCAL_STORAGE_DIR, exist_ok=True)
        file_path = os.path.join(LOCAL_STORAGE_DIR, f"{state_id}_state.txt")
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as f:
                    context = f.read()
                self.logger.debug(f"Retrieved local state from {file_path}")
                return context
            except Exception as e:
                self.logger.error(f"Error reading local state file: {e}", exc_info=True)
        else:
            self.logger.debug(f"No local state file found at {file_path}")
        return None

    def _store_local_state(self, state_id: str, data: Any) -> bool:
        """
        Store stateful memory to local storage.
        """
        os.makedirs(LOCAL_STORAGE_DIR, exist_ok=True)
        file_path = os.path.join(LOCAL_STORAGE_DIR, f"{state_id}_state.txt")
        try:
            with open(file_path, "w") as f:
                f.write(str(data))
            self.logger.debug(f"Stored local state to {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error writing to local state file: {e}", exc_info=True)
            return False

    # In-memory storage methods for stateful memory
    def _retrieve_in_memory_state(self, state_id: str) -> Optional[str]:
        """
        Retrieve stateful memory from in-memory storage.
        """
        return self.memory.in_memory_state.get(state_id)

    def _store_in_memory_state(self, state_id: str, data: Any) -> bool:
        """
        Store stateful memory to in-memory storage.
        """
        self.memory.in_memory_state[state_id] = data
        self.logger.debug(f"Stored in-memory state for state_id: {state_id}")
        return True

    # Pickle storage methods
    def _retrieve_pickle_state(self, state_id: str) -> Optional[str]:
        """
        Retrieve stateful memory from pickle storage.
        """
        os.makedirs(PICKLE_STORAGE_DIR, exist_ok=True)
        file_path = os.path.join(PICKLE_STORAGE_DIR, f"{state_id}_state.pkl")
        if os.path.exists(file_path):
            try:
                with open(file_path, "rb") as f:
                    context = pickle.load(f)
                self.logger.debug(f"Retrieved pickle state from {file_path}")
                return context
            except Exception as e:
                self.logger.error(f"Error reading pickle state file: {e}", exc_info=True)
        else:
            self.logger.debug(f"No pickle state file found at {file_path}")
        return None

    def _store_pickle_state(self, state_id: str, data: Any) -> bool:
        """
        Store stateful memory to pickle storage.
        """
        os.makedirs(PICKLE_STORAGE_DIR, exist_ok=True)
        file_path = os.path.join(PICKLE_STORAGE_DIR, f"{state_id}_state.pkl")
        try:
            with open(file_path, "wb") as f:
                pickle.dump(data, f)
            self.logger.debug(f"Stored pickle state to {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error writing to pickle state file: {e}", exc_info=True)
            return False

    # Placeholder for database storage methods
    # def _retrieve_database_state(self, state_id: str) -> Optional[str]:
    #     """
    #     Retrieve stateful memory from a database.
    #     """
    #     # Implement database retrieval logic here
    #     pass

    # def _store_database_state(self, state_id: str, data: Any) -> bool:
    #     """
    #     Store stateful memory to a database.
    #     """
    #     # Implement database storage logic here
    #     pass
