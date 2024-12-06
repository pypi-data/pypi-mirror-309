# from textarena.core import ObservationWrapper, Env, Observations, Info
# from typing import Dict, Optional, Tuple, Tuple

# __all__ = [
#     "LLMObservationWrapper"
# ]


# class LLMObservationWrapper(ObservationWrapper):
#     """TODO"""

#     def __init__(self, env: Env):
#         """TODO"""
#         super().__init__(env)
#         self.full_observations = {}

#     def reset(self, seed: Optional[int] = None) -> Observations:
#         """TODO"""
#         observations = self.env.reset(seed=seed)
#         self.full_observations = observations.copy() if observations else {}
#         return self._convert_obs_to_str()

#     def _convert_obs_to_str(self):
#         """ TODO """
#         return_dict = {}
#         for recipient_id, message_tuple in self.full_observations.items():
#             if recipient_id not in return_dict:
#                 return_dict[recipient_id] = ""
            
#             for sender_id, message in message_tuple:
#                 if sender_id in self.state.role_mapping:
#                     sender_name = self.state.role_mapping[sender_id]
#                 else:
#                     sender_name = f"Player {sender_id}"
#                 return_dict[recipient_id] += f"\n[{sender_name}] {message}"
#         return return_dict 


#     def _convert_obs_to_str(self):
#         """ TODO """
#         return_dict = {}
#         for recipient_id, message_tuple in self.full_observations.items():
#             if recipient_id not in return_dict:
#                 return_dict[recipient_id] = ""
            
#             for sender_id, message in message_tuple:
#                 if sender_id in self.state.role_mapping:
#                     sender_name = self.state.role_mapping[sender_id]
#                 else:
#                     sender_name = f"Player {sender_id}"
#                 return_dict[recipient_id] += f"\n[{sender_name}] {message}"

#             if recipient_id in self.state.role_mapping:
#                 recipient_name = self.state.role_mapping[recipient_id]
#             else:
#                 recipient_name = f"Player {recipient_id}"
#             return_dict[recipient_id] += f"\n[{recipient_name}]"
#         return return_dict 


#     def observation(
#         self, observations: Optional[Observations]  # player-wise observations
#     ) -> Optional[Observations]:  # full player-wise observations
#         # """ TODO """
#         if observations is None:
#             return self.full_observations

#         # Extend the full observations with the current observations
#         for player_id, obs in observations.items():
#             if player_id in self.full_observations:
#                 self.full_observations[player_id] += obs
#             else:
#                 self.full_observations[player_id] = obs


#         return self._convert_obs_to_str()
import textarena as ta 
from textarena.core import ObservationWrapper, Env, Observations, Info
from typing import Dict, Optional, Tuple, List

__all__ = [
    "LLMObservationWrapper"
]


class LLMObservationWrapper(ObservationWrapper):
    """
    A wrapper for converting environment observations into formatted strings suitable
    for large language models (LLMs). It ensures that duplicate observations are not
    added to the full observations.
    """

    def __init__(self, env: Env):
        """
        Initializes the LLMObservationWrapper.

        Args:
            env (Env): The environment to wrap.
        """
        super().__init__(env)
        self.full_observations: Dict[int, List[Tuple[int, str]]] = {}
        self.state = self.env.state

    def reset(self, seed: Optional[int] = None) -> Observations:
        """
        Resets the environment and initializes full observations.

        Args:
            seed (Optional[int]): Optional seed for the environment reset.

        Returns:
            Observations: The initial observations as formatted strings.
        """
        observations = self.env.reset(seed=seed)
        self.full_observations = observations.copy() if observations else {}
        return self._convert_obs_to_str()

    def _convert_obs_to_str(self) -> Observations:
        """
        Converts the full observations into formatted strings for each recipient.

        Returns:
            Observations: A dictionary mapping recipient IDs to their formatted observation strings.
        """
        return_dict: Observations = {}
        for recipient_id, message_tuples in self.full_observations.items():
            if recipient_id not in return_dict:
                return_dict[recipient_id] = ""

            for sender_id, message in message_tuples:
                if sender_id == ta.GAME_ID:
                    sender_name = "GAME"
                else:
                    sender_name = self.state.role_mapping.get(sender_id, f"Player {sender_id}")
                return_dict[recipient_id] += f"\n[{sender_name}] {message}"

            recipient_name = self.state.role_mapping.get(recipient_id, f"Player {recipient_id}")
            return_dict[recipient_id] += f"\n[{recipient_name}]"

        return return_dict

    def observation(
        self, observations: Optional[Observations]
    ) -> Optional[Observations]:
        """
        Processes new observations, ensuring no duplicates are added.

        Args:
            observations (Optional[Observations]): New player-wise observations.

        Returns:
            Optional[Observations]: The updated full observations as formatted strings.
        """
        if observations is None:
            return self._convert_obs_to_str()

        # Extend the full observations with the current observations without duplicates
        for player_id, new_obs in observations.items():
            if player_id not in self.full_observations:
                self.full_observations[player_id] = []
            
            for obs in new_obs:
                if obs not in self.full_observations[player_id]:
                    self.full_observations[player_id].append(obs)

        return self._convert_obs_to_str()
