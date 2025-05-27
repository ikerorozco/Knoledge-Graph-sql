import unittest
from unittest.mock import patch, MagicMock
from models.paper import Paper
from models.author import Author
from models.organization import Organization
from src.api.openalex_api import (
    buscar_por_titulo_openalex,
    complementar_autor_con_openalex,
    complementar_organizacion_con_openalex
)


class TestOpenAlexAPI(unittest.TestCase):

    @patch("src.api.openalex_api.requests.get")
    def test_buscar_por_titulo_openalex_string(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [{
                "title": "Test Title",
                "doi": "10.1234/abc",
                "publication_date": "2023-01-01",
                "language": "en",
                "cited_by_count": 15,
                "biblio": {"pages": "1-10"},
                "type": "journal-article",
                "authorships": [
                    {
                        "author": {
                            "display_name": "John Smith",
                            "type": "Person",
                            "affiliation": {"name": "University A"},
                            "works_count": 20
                        },
                        "institutions": [
                            {
                                "display_name": "University A",
                                "country_code": "ES",
                                "type": "education",
                                "works_count": 300,
                                "id": "https://openalex.org/I123456"
                            }
                        ]
                    }
                ]
            }]
        }
        mock_get.return_value = mock_response

        paper = buscar_por_titulo_openalex("Test Title")
        self.assertIsInstance(paper, Paper)
        self.assertEqual(paper.title, "Test Title")
        self.assertEqual(paper.doi, "10.1234/abc")
        self.assertEqual(paper.veces_citado, 15)
        self.assertEqual(len(paper.autores), 1)
        self.assertEqual(paper.autores[0].nombre, "John Smith")
        self.assertEqual(len(paper.organization), 1)
        self.assertEqual(paper.organization[0].nombre, "University A")

    @patch("src.api.openalex_api.requests.get")
    def test_buscar_por_titulo_openalex_paper(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [{
                "title": "Updated Paper",
                "doi": "10.9999/paper",
                "publication_date": "2022-05-20",
                "language": "es",
                "cited_by_count": 5,
                "biblio": {"pages": "5-10"},
                "type": "conference-paper",
                "authorships": [],
            }]
        }
        mock_get.return_value = mock_response

        input_paper = Paper(title="Original Title", doi=None, date=None,
                            idioma=None, veces_citado=None, paginas=None, rdf_type=None,
                            autores=[], organization=[])

        paper = buscar_por_titulo_openalex(input_paper)
        self.assertEqual(paper.doi, "10.9999/paper")
        self.assertEqual(paper.rdf_type, "conference-paper")
        self.assertEqual(paper.date, "2022-05-20")

    @patch("src.api.openalex_api.requests.get")
    def test_complementar_autor_con_openalex(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [{
                "type": "Person",
                "works_count": 42,
                "last_known_institution": {"display_name": "Test Institute"}
            }]
        }
        mock_get.return_value = mock_response

        autor = Author(nombre="Test Author", rdf_type=None, profesion=None, trabajos=None)
        autor_actualizado = complementar_autor_con_openalex(autor)

        self.assertEqual(autor_actualizado.rdf_type, "Person")
        self.assertEqual(autor_actualizado.trabajos, 42)
        self.assertEqual(autor_actualizado.profesion, "Test Institute")

    @patch("src.api.openalex_api.requests.get")
    def test_complementar_organizacion_con_openalex(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [{
                "type": "education",
                "country_code": "CO",
                "works_count": 500,
                "id": "https://openalex.org/I654321"
            }]
        }
        mock_get.return_value = mock_response

        org = Organization(nombre="OrgX", lugar=None, rdftype=None, trabajos=None, links=None)
        org_actualizada = complementar_organizacion_con_openalex(org)

        self.assertEqual(org_actualizada.rdftype, "education")
        self.assertEqual(org_actualizada.lugar, "CO")
        self.assertEqual(org_actualizada.trabajos, 500)
        self.assertEqual(org_actualizada.links, "https://openalex.org/I654321")


if __name__ == "__main__":
    unittest.main()
