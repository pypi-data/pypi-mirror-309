import inspect
import json
import logging
import os
import string
from typing import Any, Dict, List, Optional


class LocoJSON:
    def __init__(self, locale: str, fallback_locale: str = "en", locale_dir: str = "loc", log_level: int = logging.WARNING):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        handler = logging.StreamHandler()
        handler.setFormatter(_ColorFormatter("\033[92m%(asctime)s\033[0m | %(levelname)s\t | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
        self.logger.addHandler(handler)

        self.formatter = _SafeFormatter(self.logger)
        self.locale = locale
        self.fallback_locale = fallback_locale
        self.locale_dir = locale_dir
        self.translations: Dict[str, Dict[str, Any]] = {}
        self.cache: Dict[str, Dict[str, Any]] = {}

        self._load_translations(fallback_locale)
        self._load_translations(locale)

    def __getattr__(self, key: str) -> "_LocoDict":
        return _LocoDict(self, [key])

    def change_locale(self, locale: str) -> None:
        """ Change the locale and load the translations for the new locale """
        self.locale = locale
        self._load_translations(locale)

    def change_fallback_locale(self, fallback_locale: str) -> None:
        """ Change the fallback locale """
        self.fallback_locale = fallback_locale
        self._load_translations(fallback_locale)

    def clear_cache(self) -> None:
        """ Clear the cache """
        self.cache = {}

    def get_current_locale(self) -> str:
        """ Get the current locale """
        return self.locale

    def _load_translations(self, locale: str) -> None:
        if locale in self.cache:
            self.translations[locale] = self.cache[locale]
            return

        locale_file = os.path.join(self.locale_dir, f"{locale}.json")
        if os.path.exists(locale_file):
            try:
                with open(locale_file, "r", encoding="utf-8") as f:
                    self.translations[locale] = json.load(f)
                    self.cache[locale] = self.translations[locale]
                self.logger.info(f"Loaded JSON file for locale {locale}")
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to load JSON file for locale {locale}: {e}")

    def _get_translation(self, keys: List[str], locale: str, **kwargs) -> str:
        if locale not in self.translations:
            self._load_translations(locale)

        translation: Any = self.translations.get(locale, {})
        for k in keys:
            if isinstance(translation, Dict):
                translation = translation.get(k)
            else:
                translation = None
            if translation is None:
                break

        if translation is None and locale != self.fallback_locale:
            frame = inspect.stack()[-1]
            if locale != self.fallback_locale:
                self.logger.warning(f"{os.path.relpath(frame.filename)}:{frame.lineno} - Missing translation: \033[94m{'.'.join(keys)}\033[0m in: \033[94m{locale}\033[0m, falling back to \033[94m{self.fallback_locale}\033[0m")
                return self._get_translation(keys, self.fallback_locale, **kwargs)
            else:
                self.logger.warning(f"{os.path.relpath(frame.filename)}:{frame.lineno} - Missing translation: \033[94m{'.'.join(keys)}\033[0m in: \033[94m{locale}\033[0m, return key name")
                return ".".join(keys)

        if translation is not None and isinstance(translation, str):
            used_keys = {field_name for _, field_name, _, _ in self.formatter.parse(translation) if field_name}
            unused_keys = {key: value for key, value in kwargs.items() if key not in used_keys}
            if unused_keys:
                frame = inspect.stack()[-1]
                self.logger.warning(f"{os.path.relpath(frame.filename)}:{frame.lineno} - Unused keys: {unused_keys}")
            return self.formatter.format(translation, **kwargs)
        else:
            frame = inspect.stack()[-1]
            self.logger.warning(f"{os.path.relpath(frame.filename)}:{frame.lineno} - Missing translation: \033[94m{'.'.join(keys)}\033[0m in: \033[94m{locale}\033[0m, return key name")
            return ".".join(keys)


class _LocoDict:
    def __init__(self, localization: LocoJSON, keys: List[str]):
        self.localization = localization
        self.keys = keys

    def __getattr__(self, key: str) -> "_LocoDict":
        return _LocoDict(self.localization, self.keys + [key])

    def __call__(self, locale: Optional[str] = None, **kwargs) -> str:
        if locale is None:
            locale = self.localization.locale
        return self.localization._get_translation(self.keys, locale, **kwargs)


class _SafeFormatter(string.Formatter):
    def __init__(self, logger: logging.Logger):
        super().__init__()
        self.logger = logger

    def get_value(self, key, args, kwargs) -> Any:
        if isinstance(key, str):
            if key not in kwargs:
                frame = inspect.stack()[-1]
                self.logger.warning(f"{os.path.relpath(frame.filename)}:{frame.lineno} - Missing placeholder: \033[94m{key}\033[0m")
            return kwargs.get(key, "{" + key + "}")
        return string.Formatter.get_value(self, key, args, kwargs)


class _ColorFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[94m",
        "INFO": "\033[92m",
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
        "CRITICAL": "\033[95m"
    }
    RESET = "\033[0m"

    def format(self, record):
        record.levelname = f"{self.COLORS.get(record.levelname, self.RESET)}{record.levelname}{self.RESET}"
        return super().format(record)