import networkx as nx
from models.paper import Paper
from models.author import Author
from models.organization import Organization
from models.project import Project
import matplotlib.pyplot as plt
from typing import List, Dict, Any, Optional
import matplotlib.patches as mpatches
from rdflib import Graph, Literal, URIRef, Namespace
from rdflib.namespace import RDF, RDFS, XSD, FOAF, DC

class KnowledgeGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        
    def add_papers(self, papers: List[Paper]):
        """
        Add papers and their relationships to the knowledge graph.
        
        Args:
            papers: List of Paper objects to add to the graph
        """
        for paper in papers:
            # Add paper node
            self.graph.add_node(paper.title, type="paper", data=paper)
            
            # Add authors and their relationships (author -> paper: authored)
            if paper.autores:
                for author in paper.autores:
                    author_id = author.nombre
                    self.graph.add_node(author_id, type="author", data=author)
                    # Direction: author authored paper
                    self.graph.add_edge(author_id, paper.title, relationship="authored")
                    # Also add reverse direction for easier querying
                    self.graph.add_edge(paper.title, author_id, relationship="has_author")
            
            # Add organizations and their relationships (org -> paper: affiliated_with)
            if paper.organization:
                for org in paper.organization:
                    org_id = org.nombre
                    self.graph.add_node(org_id, type="organization", data=org)
                    # Direction: organization affiliated_with paper
                    self.graph.add_edge(org_id, paper.title, relationship="affiliated_with")
            
            
            # Also check the papersSimilares attribute that exists in the model
            if hasattr(paper, 'papersSimilares') and paper.papersSimilares:
                for similar_paper in paper.papersSimilares:
                    if isinstance(similar_paper, Paper) and similar_paper.title:
                        self.graph.add_node(similar_paper.title, type="paper", data=similar_paper)
                        self.graph.add_edge(paper.title, similar_paper.title, relationship="similar_to")
    
    def add_projects(self, projects: List[Project], papers: List[Paper]):
        """
        Add projects and their relationships to papers in the knowledge graph.
        
        Args:
            projects: List of Project objects
            papers: List of Paper objects to link with projects
        """
        paper_titles = {paper.title: paper for paper in papers}
        
        for project in projects:
            # Use nombre attribute from the Project model
            project_id = project.nombre
            self.graph.add_node(project_id, type="project", data=project)
            
            # Link projects to papers if the project has papers associated
            if hasattr(project, 'papers') and project.papers:
                for paper in project.papers:
                    if isinstance(paper, Paper) and paper.title:
                        # Direction: project funded paper
                        self.graph.add_edge(project_id, paper.title, relationship="funded")
            
            # Additional check: for any paper that mentions this project
            for title, paper in paper_titles.items():
                # This could be expanded based on how papers reference projects in your system
                # For now, just checking if the project name appears in the paper title (simple heuristic)
                if project.nombre.lower() in title.lower():
                    # Direction: project related_to paper
                    self.graph.add_edge(project_id, title, relationship="related_to")
    
    def visualize(self, figsize=(12, 10), include_labels=True, node_size=1500, font_size=8, save_path="knowledge_graph.png"):
        """
        Visualize the knowledge graph. Saves the graph as an image file.
        
        Args:
            figsize: Size of the figure (width, height)
            include_labels: Whether to include node labels
            node_size: Size of nodes
            font_size: Size of labels font
            save_path: Path where to save the visualization image
        """
        plt.figure(figsize=figsize)
        
        # Create node colors based on type
        node_colors = []
        node_sizes = []
        
        # Define color mapping for node types
        color_map = {
            'paper': 'skyblue',
            'author': 'lightgreen',
            'organization': 'salmon',
            'project': 'yellow',
            'default': 'gray'
        }
        
        for node in self.graph.nodes():
            node_type = self.graph.nodes[node].get('type', '')
            if node_type in color_map:
                node_colors.append(color_map[node_type])
                if node_type == 'paper':
                    node_sizes.append(node_size)
                elif node_type == 'author':
                    node_sizes.append(node_size * 0.8)
                elif node_type == 'organization':
                    node_sizes.append(node_size * 1.2)
                elif node_type == 'project':
                    node_sizes.append(node_size * 1.2)
                else:
                    node_sizes.append(node_size * 0.7)
            else:
                node_colors.append(color_map['default'])
                node_sizes.append(node_size * 0.7)
        
        # Create edge colors based on relationship type
        edge_colors = []
        
        # Define color mapping for edge types
        edge_color_map = {
            'authored': 'green',
            'has_author': 'green',
            'affiliated_with': 'red',
            'has_organization': 'red',
            'similar_to': 'blue',
            'funded': 'orange',
            'related_to': 'purple',
            'default': 'gray'
        }
        
        for _, _, edge_data in self.graph.edges(data=True):
            relationship = edge_data.get('relationship', '')
            if relationship in edge_color_map:
                edge_colors.append(edge_color_map[relationship])
            else:
                edge_colors.append(edge_color_map['default'])
        
        # Draw the graph
        pos = nx.spring_layout(self.graph, k=0.5, iterations=50)  # Adjust layout for better visualization
        
        # Draw nodes
        nx.draw_networkx_nodes(
            self.graph, pos, 
            node_color=node_colors, 
            node_size=node_sizes,
            alpha=0.8
        )
        
        # Draw edges with colors
        nx.draw_networkx_edges(
            self.graph, pos, 
            edge_color=edge_colors, 
            width=1.0,
            alpha=0.6,
            arrows=True,
            arrowsize=10,
            connectionstyle='arc3,rad=0.1'  # Curved edges for better visualization
        )
        
        # Add edge labels showing relationship types
        edge_labels = {}
        for u, v, edge_data in self.graph.edges(data=True):
            relationship = edge_data.get('relationship', '')
            edge_labels[(u, v)] = relationship
        
        # Draw edge labels with smaller font and slight offset
        nx.draw_networkx_edge_labels(
            self.graph, pos,
            edge_labels=edge_labels,
            font_size=font_size-2,
            font_color='black',
            font_family='sans-serif',
            alpha=0.7,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.7),
            label_pos=0.5,  # Centered on the edge
            rotate=False    # Don't rotate labels
        )
        
        # Draw labels if requested
        if include_labels:
            # Create custom labels with shorter text
            labels = {}
            for node in self.graph.nodes():
                # Truncate long labels for better visualization
                if len(str(node)) > 20:
                    labels[node] = str(node)[:17] + "..."
                else:
                    labels[node] = node
                    
            nx.draw_networkx_labels(
                self.graph, pos, 
                labels=labels,
                font_size=font_size, 
                font_weight='bold'
            )
        
        # Create legend for node types
        legend_elements = [
            mpatches.Patch(color=color_map['paper'], label='Paper'),
            mpatches.Patch(color=color_map['author'], label='Author'),
            mpatches.Patch(color=color_map['organization'], label='Organization'),
            mpatches.Patch(color=color_map['project'], label='Project')
        ]
        
        # Add legend for edge types
        edge_legend_elements = [
            mpatches.Patch(color=edge_color_map['authored'], label='Authored/Has Author'),
            mpatches.Patch(color=edge_color_map['affiliated_with'], label='Affiliated With/Has Organization'),
            mpatches.Patch(color=edge_color_map['similar_to'], label='Similar To'),
            mpatches.Patch(color=edge_color_map['funded'], label='Funded'),
            mpatches.Patch(color=edge_color_map['related_to'], label='Related To')
        ]
        
        # Combine both legends
        all_legend_elements = legend_elements + edge_legend_elements
        
        # Add the legend to the plot with a title
        plt.legend(handles=legend_elements, title="Node Types", loc="upper left", bbox_to_anchor=(1, 1))
        
        plt.title("Knowledge Graph")
        plt.axis('off')  # Hide axis
        plt.tight_layout()
        
        # Save the figure to a file instead of showing it
        print(f"Saving knowledge graph visualization to {save_path}")
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return save_path
    
    def export_to_rdf(self, output_file: str):
        """
        Export the knowledge graph to RDF format.
        
        Args:
            output_file: Path to the output RDF file
        """
        # Create an RDF graph
        rdf_graph = Graph()
        
        # Define namespaces
        KG = Namespace("http://knowledge-graph.org/")
        PAPER = Namespace("http://knowledge-graph.org/paper/")
        AUTHOR = Namespace("http://knowledge-graph.org/author/")
        ORG = Namespace("http://knowledge-graph.org/organization/")
        PROJECT = Namespace("http://knowledge-graph.org/project/")
        
        # Bind namespaces to prefixes for better readability
        rdf_graph.bind("kg", KG)
        rdf_graph.bind("paper", PAPER)
        rdf_graph.bind("author", AUTHOR)
        rdf_graph.bind("org", ORG)
        rdf_graph.bind("project", PROJECT)
        rdf_graph.bind("foaf", FOAF)
        rdf_graph.bind("dc", DC)
        
        # Helper function to create a URI-safe ID
        def uri_safe(name: str) -> str:
            return name.replace(" ", "_").replace("/", "_").replace(":", "_").replace(",", "_").replace(".", "_")
        
        # Process all nodes in the graph
        for node, data in self.graph.nodes(data=True):
            node_type = data.get('type', '')
            node_data = data.get('data')
            
            if node_type == 'paper' and node_data:
                # Create paper URI
                paper_uri = PAPER[uri_safe(node)]
                
                # Add paper triples
                rdf_graph.add((paper_uri, RDF.type, KG.Paper))
                rdf_graph.add((paper_uri, DC.title, Literal(node_data.title)))
                
                if node_data.doi:
                    rdf_graph.add((paper_uri, DC.identifier, Literal(node_data.doi)))
                
                if node_data.date:
                    rdf_graph.add((paper_uri, DC.date, Literal(node_data.date)))
                
                if node_data.idioma:
                    rdf_graph.add((paper_uri, DC.language, Literal(node_data.idioma)))
                
                if node_data.veces_citado:
                    rdf_graph.add((paper_uri, KG.timesCited, Literal(node_data.veces_citado, datatype=XSD.integer)))
                
                if node_data.paginas:
                    rdf_graph.add((paper_uri, KG.pages, Literal(node_data.paginas, datatype=XSD.integer)))
            
            elif node_type == 'author' and node_data:
                # Create author URI
                author_uri = AUTHOR[uri_safe(node)]
                
                # Add author triples
                rdf_graph.add((author_uri, RDF.type, KG.Author))
                rdf_graph.add((author_uri, FOAF.name, Literal(node_data.nombre)))
                
                if node_data.profesion:
                    rdf_graph.add((author_uri, KG.profession, Literal(node_data.profesion)))
                
                if node_data.trabajos:
                    rdf_graph.add((author_uri, KG.works, Literal(node_data.trabajos, datatype=XSD.integer)))
            
            elif node_type == 'organization' and node_data:
                # Create organization URI
                org_uri = ORG[uri_safe(node)]
                
                # Add organization triples
                rdf_graph.add((org_uri, RDF.type, KG.Organization))
                rdf_graph.add((org_uri, FOAF.name, Literal(node_data.nombre)))
                
                if node_data.lugar:
                    rdf_graph.add((org_uri, KG.location, Literal(node_data.lugar)))
                
                if node_data.trabajos:
                    rdf_graph.add((org_uri, KG.works, Literal(node_data.trabajos, datatype=XSD.integer)))
                
                if hasattr(node_data, 'links') and node_data.links:
                    for link in node_data.links:
                        rdf_graph.add((org_uri, FOAF.page, URIRef(link)))
            
            elif node_type == 'project' and node_data:
                # Create project URI
                project_uri = PROJECT[uri_safe(node)]
                
                # Add project triples
                rdf_graph.add((project_uri, RDF.type, KG.Project))
                rdf_graph.add((project_uri, DC.title, Literal(node_data.nombre)))
                
                if node_data.fundedAmount:
                    rdf_graph.add((project_uri, KG.fundedAmount, Literal(node_data.fundedAmount, datatype=XSD.decimal)))
                
                if node_data.startdate:
                    rdf_graph.add((project_uri, KG.startDate, Literal(node_data.startdate.isoformat(), datatype=XSD.date)))
                
                if node_data.enddate:
                    rdf_graph.add((project_uri, KG.endDate, Literal(node_data.enddate.isoformat(), datatype=XSD.date)))
        
        # Process all edges (relationships) in the graph
        for source, target, edge_data in self.graph.edges(data=True):
            relationship = edge_data.get('relationship', '')
            
            # Skip if no relationship is defined
            if not relationship:
                continue
            
            # Get source and target node types
            source_type = self.graph.nodes[source].get('type', '')
            target_type = self.graph.nodes[target].get('type', '')
            
            # Create URIs for source and target
            source_uri = None
            target_uri = None
            
            if source_type == 'paper':
                source_uri = PAPER[uri_safe(source)]
            elif source_type == 'author':
                source_uri = AUTHOR[uri_safe(source)]
            elif source_type == 'organization':
                source_uri = ORG[uri_safe(source)]
            elif source_type == 'project':
                source_uri = PROJECT[uri_safe(source)]
                
            if target_type == 'paper':
                target_uri = PAPER[uri_safe(target)]
            elif target_type == 'author':
                target_uri = AUTHOR[uri_safe(target)]
            elif target_type == 'organization':
                target_uri = ORG[uri_safe(target)]
            elif target_type == 'project':
                target_uri = PROJECT[uri_safe(target)]
            
            # Add relationship triple if both URIs are valid
            if source_uri and target_uri:
                # Map relationship types to RDF predicates
                if relationship == 'authored':
                    rdf_graph.add((source_uri, KG.authored, target_uri))
                elif relationship == 'has_author':
                    rdf_graph.add((source_uri, KG.hasAuthor, target_uri))
                elif relationship == 'affiliated_with':
                    rdf_graph.add((source_uri, KG.affiliatedWith, target_uri))
                elif relationship == 'has_organization':
                    rdf_graph.add((source_uri, KG.hasOrganization, target_uri))
                elif relationship == 'similar_to':
                    rdf_graph.add((source_uri, KG.similarTo, target_uri))
                elif relationship == 'funded':
                    rdf_graph.add((source_uri, KG.funded, target_uri))
                elif relationship == 'related_to':
                    rdf_graph.add((source_uri, KG.relatedTo, target_uri))
        
        # Serialize the RDF graph to file
        print(f"Saving RDF graph to {output_file}")
        rdf_graph.serialize(destination=output_file, format="turtle")
        
        return output_file
    
    def query_graph(self, query_type: str, query_params: Dict[str, Any]):
        """
        Query the knowledge graph.
        
        Args:
            query_type: Type of query (e.g., "authors_of_paper", "papers_by_organization", 
                                       "projects_of_paper", "papers_by_author", "similar_papers")
            query_params: Parameters for the query
            
        Returns:
            List of query results
        """
        results = []
        
        if query_type == "authors_of_paper":
            paper_title = query_params.get("paper_title")
            # Look for direct edges from paper to author
            for _, author, edge_data in self.graph.out_edges(paper_title, data=True):
                if edge_data.get("relationship") == "has_author":
                    author_data = self.graph.nodes[author].get("data")
                    if author_data:
                        results.append(author_data)
        
        elif query_type == "papers_by_author":
            author_name = query_params.get("author_name")
            # Look for direct edges from author to paper
            for _, paper, edge_data in self.graph.out_edges(author_name, data=True):
                if edge_data.get("relationship") == "authored":
                    paper_data = self.graph.nodes[paper].get("data")
                    if paper_data:
                        results.append(paper_data)
        
        elif query_type == "papers_by_organization":
            org_name = query_params.get("organization_name")
            # Look for direct edges from organization to paper
            for _, paper, edge_data in self.graph.out_edges(org_name, data=True):
                if edge_data.get("relationship") == "affiliated_with":
                    paper_data = self.graph.nodes[paper].get("data")
                    if paper_data:
                        results.append(paper_data)
        
        elif query_type == "organizations_of_paper":
            paper_title = query_params.get("paper_title")
            # Look for direct edges from paper to organization
            for _, org, edge_data in self.graph.out_edges(paper_title, data=True):
                if edge_data.get("relationship") == "has_organization":
                    org_data = self.graph.nodes[org].get("data")
                    if org_data:
                        results.append(org_data)
        
        elif query_type == "papers_by_project":
            project_name = query_params.get("project_name")
            # Look for direct edges from project to paper
            for _, paper, edge_data in self.graph.out_edges(project_name, data=True):
                if edge_data.get("relationship") == "funded":
                    paper_data = self.graph.nodes[paper].get("data")
                    if paper_data:
                        results.append(paper_data)
        
        elif query_type == "similar_papers":
            paper_title = query_params.get("paper_title")
            # Look for direct edges from paper to similar papers
            for _, similar, edge_data in self.graph.out_edges(paper_title, data=True):
                if edge_data.get("relationship") == "similar_to":
                    similar_data = self.graph.nodes[similar].get("data")
                    if similar_data:
                        results.append(similar_data)
        
        return results

def create_knowledge_graph(papers: List[Paper], projects: Optional[List[Project]] = None):
    """
    Create a knowledge graph from papers and projects.
    
    Args:
        papers: List of Paper objects
        projects: Optional list of Project objects
        
    Returns:
        KnowledgeGraph object
    """
    kg = KnowledgeGraph()
    kg.add_papers(papers)
    
    if projects:
        kg.add_projects(projects, papers)
    
    return kg 