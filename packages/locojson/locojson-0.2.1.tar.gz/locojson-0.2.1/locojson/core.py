import os
import json
from lococore import LocoCore


class LocoJSON(LocoCore):
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