from collections import deque
from collections.abc import Iterable
from logging import warn
from typing import Any, Deque, Optional, SupportsFloat, TypeVar

from gymnasium import Env, Wrapper, utils

ObsType = TypeVar("ObsType")
ActType = TypeVar("ActType")


def _compact_dicts(
    dicts: Iterable[dict[str, Any]], fill_value: Any = None
) -> dict[str, list[Any]]:
    """Compacts an iterable of dictionaries into a single dict with lists of entries. If
    an entry is missing for any given dict, ``fill_value`` is used in place.

    Parameters
    ----------
    dicts : iterable of dicts of (str, any)
        Dictionaries to be compacted into a single one.
    fill_value : any, optional
        The value to be used to fill in missing values.

    Returns
    -------
    dict of (str, list of any | fill_value)
        A unique dictionary made from all the passed dicts.
    """
    out: dict[str, list[Any]] = {}
    for i, dict_ in enumerate(dicts):
        for k, v in dict_.items():
            if k in out:
                out[k].append(v)
            else:
                out[k] = [fill_value] * i + [v]
        for k in out.keys() - dict_.keys():
            out[k].append(fill_value)
    return out


class MonitorInfos(
    Wrapper[ObsType, ActType, ObsType, ActType], utils.RecordConstructorArgs
):
    """This wrapper keeps track of the infos that are generated by calls to
    :func:`gymnasium.Env.reset` and :func:`gymnasium.Env.step`.

    Parameters
    ----------
    env : Env[ObsType, ActType]
        The environment to apply the wrapper to.
    deque_size : int, optional
        The maximum number of episodes to hold as historical data in the internal
        deques. By default, ``None``, i.e., unlimited.
    """

    def __init__(
        self, env: Env[ObsType, ActType], deque_size: Optional[int] = None
    ) -> None:
        utils.RecordConstructorArgs.__init__(self, deque_size=deque_size)
        Wrapper.__init__(self, env)
        # long-term storages
        self.reset_infos: Deque[dict[str, Any]] = deque(maxlen=deque_size)
        self.step_infos: Deque[list[dict[str, Any]]] = deque(maxlen=deque_size)
        # current-episode storages
        self.ep_step_infos: list[dict[str, Any]] = []

    def reset(
        self, *, seed: Optional[int] = None, options: Optional[dict[str, Any]] = None
    ) -> tuple[ObsType, dict[str, Any]]:
        observation, info = super().reset(seed=seed, options=options)
        self.ep_step_infos.clear()
        self.reset_infos.append(info)
        return observation, info

    def step(
        self, action: ActType
    ) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:
        obs, reward, terminated, truncated, info = super().step(action)
        self.ep_step_infos.append(info)
        if terminated or truncated:
            self.step_infos.append(self.ep_step_infos.copy())
            self.ep_step_infos.clear()
        return obs, reward, terminated, truncated, info

    def finalized_reset_infos(self, fill_value: Any = None) -> dict[str, list[Any]]:
        """Returns a compacted final dictionary containing the reset infos. Missing
        values are filled automatically.

        Parameters
        ----------
        fill_value : Any, optional
            The value to be used to fill in missing values.

        Returns
        -------
        dict of (str, list)
            A unique dict containing for each entry returned in the reset info the
            corresponding list of entries, one per each reset call.
        """
        return _compact_dicts(self.reset_infos, fill_value)

    def finalized_step_infos(
        self, fill_value: Any = None
    ) -> dict[str, list[list[Any]]]:
        """Returns a compacted final dictionary containing the step infos. Missing
        values are filled automatically.

        Parameters
        ----------
        fill_value : Any, optional
            The value to be used to fill in missing values.

        Returns
        -------
        dict of (str, list of lists)
            A unique dict containing for each entry returned in the step info the
            corresponding list of dicts per episode, with one entry per each step call.
        """

        if self.ep_step_infos:
            warn(
                "Internal buffer of step infos not empty, meaning that the last "
                "episode did not terminate properly.",
                RuntimeWarning,
            )
        return _compact_dicts(
            (_compact_dicts(d, fill_value) for d in self.step_infos), fill_value
        )
