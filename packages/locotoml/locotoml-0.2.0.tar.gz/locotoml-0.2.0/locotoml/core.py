import os
import toml
from lococore import LocoCore

class LocoTOML(LocoCore):
    def _load_translations(self, locale: str) -> None:
        if locale in self.cache:
            self.translations[locale] = self.cache[locale]
            return

        locale_file = os.path.join(self.locale_dir, f"{locale}.toml")
        if os.path.exists(locale_file):
            try:
                with open(locale_file, "r", encoding="utf-8") as f:
                    self.translations[locale] = toml.load(f)
                    self.cache[locale] = self.translations[locale]
                self.logger.info(f"Loaded TOML file for locale {locale}")
            except toml.TomlDecodeError as e:
                self.logger.error(f"Failed to load TOML file for locale {locale}: {e}")