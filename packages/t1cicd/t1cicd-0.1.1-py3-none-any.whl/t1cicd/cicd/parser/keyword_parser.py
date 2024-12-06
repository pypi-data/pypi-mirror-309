from abc import ABC, abstractmethod

from t1cicd.cicd.parser.artifact import Artifact


class KeywordParser(ABC):
    @abstractmethod
    def parse(self, value):
        pass


class KeywordParserFactory(ABC):
    @abstractmethod
    def get_parser(keyword: str) -> KeywordParser:
        if keyword == "stage":
            return StageParser()
        elif keyword == "needs":
            return NeedParser()
        elif keyword == "script":
            return ScriptParser()
        elif keyword == "artifacts":
            return ArtifactsParser()
        elif keyword == "image":
            return ImageParser()
        elif keyword == "allow_failure":
            return AllowFailureParser()
        else:
            raise ValueError(f"Unknown keyword: {keyword}")


class StageParser(KeywordParser):
    def parse(self, value):
        if not isinstance(value, str):
            raise ValueError(f"Expected a string, got {type(value)}")
        return value


class NeedParser(KeywordParser):
    def parse(self, value):
        if not isinstance(value, list):
            raise ValueError(f"Expected a list, got {type(value)}")
        return value


class ScriptParser(KeywordParser):
    def parse(self, value):
        if not isinstance(value, list) and not isinstance(value, str):
            raise ValueError(f"Expected a list or string, got {type(value)}")
        return value


class ArtifactsParser(KeywordParser):
    def parse(self, value):
        if not isinstance(value, object):
            raise ValueError(f"Expected a Object, got {type(value)}")
        return Artifact(paths=value["paths"])


class ImageParser(KeywordParser):
    def parse(self, value):
        if not isinstance(value, str):
            raise ValueError(f"Expected a string, got {type(value)}")
        return value


class AllowFailureParser(KeywordParser):
    def parse(self, value):
        if not isinstance(value, bool):
            raise ValueError(f"Expected a boolean, got {type(value)}")
        return value
