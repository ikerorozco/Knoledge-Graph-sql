import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.api.openaire_api import (
    parsear_xml_openaire,
    parsear_json_organizacion_openaire,
    buscar_por_titulo,
    buscar_proyectos_por_titulo,
)
from models.paper import Paper


class TestOpenAIREParser(unittest.TestCase):

    def test_parsear_xml_openaire_valido(self):
        xml_data = """
        <root>
            <title>Sample Paper</title>
            <pid classid="doi">10.1234/example.doi</pid>
            <dateofacceptance>2024-01-01</dateofacceptance>
            <language>en</language>
            <citationcount>5</citationcount>
            <resourcetype pages="10-15">journal article</resourcetype>
            <creator>
                <creatorName>John Doe</creatorName>
                <type>Person</type>
                <occupation>Researcher</occupation>
                <affiliation>University A</affiliation>
            </creator>
        </root>
        """
        paper = parsear_xml_openaire(xml_data)
        self.assertIsInstance(paper, Paper)
        self.assertEqual(paper.title, "Sample Paper")
        self.assertEqual(paper.doi, "10.1234/example.doi")
        self.assertEqual(paper.date, "2024-01-01")
        self.assertEqual(paper.idioma, "en")
        self.assertEqual(paper.veces_citado, "5")
        self.assertEqual(paper.paginas, "10-15")
        self.assertEqual(paper.rdf_type, "journal article")
        self.assertEqual(len(paper.autores), 1)
        self.assertEqual(paper.autores[0].nombre, "John Doe")

    def test_parsear_json_organizacion_openaire(self):
        json_data = {
            "header": {"numFound": 1},
            "results": [{
                "legalName": "Org Name",
                "country": {"label": "Spain"},
                "websiteUrl": "http://example.org",
                "id": "org-123",
                "alternativeNames": ["Org Alt"]
            }]
        }
        organizaciones = parsear_json_organizacion_openaire(json_data)
        self.assertIsInstance(organizaciones, list)
        self.assertEqual(len(organizaciones), 1)
        self.assertEqual(organizaciones[0].nombre, "Org Name")

    @patch("src.api.openaire_api.requests.get")
    def test_buscar_por_titulo(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<root><title>Test</title></root>"
        mock_get.return_value = mock_response

        paper = buscar_por_titulo("Test")
        self.assertIsInstance(paper, Paper)
        self.assertEqual(paper.title, "Test")


    @patch("src.api.openaire_api.requests.get")
    def test_buscar_proyectos_por_titulo(self, mock_get):
        xml_response = """
        <root>
            <rel>
                <to class="isProducedBy" type="project">proj-123</to>
            </rel>
        </root>
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = xml_response

        paper = Paper(title="Test", doi=None, date=None, idioma=None,
                      veces_citado=None, paginas=None, rdf_type=None, autores=[], organization=[])
        project_ids = buscar_proyectos_por_titulo(paper)
        self.assertIn("proj-123", project_ids)



if __name__ == "__main__":
    unittest.main()
