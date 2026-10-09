import networkx as nx


class DependencyGraph:

    def __init__(self, analysis):
        self.analysis = analysis
        self.graph = nx.DiGraph()

    def build(self):

        functions = self.analysis.get(
            "functions",
            []
        )

        classes = self.analysis.get(
            "classes",
            []
        )

        imports = self.analysis.get(
            "imports",
            []
        )

        # --------------------------------------------------
        # ADD FUNCTION NODES
        # --------------------------------------------------

        for function in functions:

            function_name = function["name"]

            self.graph.add_node(
                function_name,
                type="function",
                line=function["line"],
                end_line=function["end_line"]
            )

        # --------------------------------------------------
        # ADD CLASS NODES
        # --------------------------------------------------

        for cls in classes:

            class_name = cls["name"]

            self.graph.add_node(
                class_name,
                type="class",
                line=cls["line"],
                end_line=cls["end_line"]
            )

        # --------------------------------------------------
        # ADD FUNCTION CALL EDGES
        # --------------------------------------------------

        function_names = {
            function["name"]
            for function in functions
        }

        for function in functions:

            source = function["name"]

            for call in function.get(
                "calls",
                []
            ):

                target = call["name"]

                # Only connect functions that
                # actually exist in our source.
                if target in function_names:

                    self.graph.add_edge(
                        source,
                        target,
                        type="calls",
                        line=call["line"]
                    )

        # --------------------------------------------------
        # ADD CLASS → METHOD RELATIONSHIPS
        # --------------------------------------------------

        for cls in classes:

            class_name = cls["name"]

            for method in cls.get(
                "methods",
                []
            ):

                method_name = method["name"]

                # Use Class.method to avoid
                # name collisions.
                full_method_name = (
                    f"{class_name}.{method_name}"
                )

                self.graph.add_node(
                    full_method_name,
                    type="method",
                    line=method["line"],
                    end_line=method["end_line"]
                )

                self.graph.add_edge(
                    class_name,
                    full_method_name,
                    type="contains"
                )

        # --------------------------------------------------
        # ADD IMPORT NODES
        # --------------------------------------------------

        for imp in imports:

            if "module" in imp:

                import_name = (
                    f"{imp['module']}."
                    f"{imp['name']}"
                )

            else:

                import_name = imp["name"]

            import_node = f"import:{import_name}"

            self.graph.add_node(
                import_node,
                type="import",
                line=imp["line"]
            )

        return self.graph

    def get_graph_data(self):

        nodes = []

        for node, data in self.graph.nodes(
            data=True
        ):

            nodes.append({
                "id": node,
                **data
            })

        edges = []

        for source, target, data in self.graph.edges(
            data=True
        ):

            edges.append({
                "source": source,
                "target": target,
                **data
            })

        return {
            "nodes": nodes,
            "edges": edges
        }