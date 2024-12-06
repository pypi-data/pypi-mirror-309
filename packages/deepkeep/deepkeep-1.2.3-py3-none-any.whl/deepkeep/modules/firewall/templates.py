from ..base_module import BaseModule


class Templates(BaseModule):
    root_path: str = "firewall"

    def get(self, firewall_id: str):
        """
        Get optional filter templates for a firewall
        """
        optional_templates = self._make_request(method="GET", path=f"{self.root_path}/{firewall_id}/filter_options")
        return optional_templates["data"]
