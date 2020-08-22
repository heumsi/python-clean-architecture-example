from domain.use_case.read_post import ReadPostOutputBoundary, ReadPostOutputDto

class OutputAdapter(ReadPostOutputBoundary):
    def execute(self, output_dto: ReadPostOutputDto) -> None:
        output_dto.to_dict()