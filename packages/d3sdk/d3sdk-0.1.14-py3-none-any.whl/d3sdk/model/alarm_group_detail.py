from typing import List

class Cause:
    def __init__(self, cause_code: str, cause_display_name: str, cause_description: str, steps: List['Step']):
        self.code = cause_code
        self.display_name = cause_display_name
        self.description = cause_description
        self.steps = steps

    def __repr__(self):
        return (f"Cause(code={self.code!r}, "
                f"display_name={self.display_name!r}, "
                f"description={self.description!r}, "
                f"steps={self.steps!r})")

class Step:
    def __init__(self, step_code: str, step_display_name: str, step_description: str):
        self.code = step_code
        self.display_name = step_display_name
        self.description = step_description

    def __repr__(self):
        return (f"Step(code={self.code!r}, "
                f"display_name={self.display_name!r}, "
                f"description={self.description!r})")

class AlarmDetail:
    """
    报警的原因建议
    """
    def __init__(self, dfem_sxmsbh: str, dfem_bjlx: str, causes: List[Cause]):
        self.dfem_sxmsbh = dfem_sxmsbh
        self.dfem_bjlx = dfem_bjlx
        self.causes = causes

    def __repr__(self):
        return (f"AlarmDetail(dfem_sxmsbh={self.dfem_sxmsbh!r}, "
                f"dfem_bjlx={self.dfem_bjlx!r}, "
                f"causes={self.causes!r})")