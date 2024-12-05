import mlflow 
# import pandas as pd 
# from mlflow.pyfunc import PythonModel  
# from mlflow.models import set_model  
from castle.algorithms import PC  
import utils
import model_scripts as scripts
import os
import networkx as nx
import matplotlib.pyplot as plt

class CausalMatrix:
    def __init__(self, 
                 algorithm, 
                 visualization_style="network", 
                 logging_target="mlflow_server", 
                 ):
        
        if algorithm not in utils.supported_algorithms:
            raise ValueError(f"Unsupported model: {algorithm}")
                
        self.visualization_style = visualization_style
        self.logging_target = logging_target
        self.algorithm=algorithm
        self.model_script_path=f"{algorithm}_causal_model.py"
        self.registered_model_name=f"{algorithm}_model"

    def discover_causal_graph(self,data):
        pc=PC()
        pc.learn(data)
        return (pc.causal_matrix)
    
    def log_causal_model(self,
                         mlflow_experimemt_name=None,
                         sample_data=None):
        if self.logging_target not in utils.supported_logging_target:
            raise ValueError(f"Unsupported logging_target: {self.logging_target}")
        
        if self.logging_target == "databricks_uc":
            if self.data is not None:
                sample_data=self.data.head()
                self.signature=self._infer_signature(sample_data)
            else:
                raise ValueError(f"sample_data is required to create a model signature for {self.logging_target}")
        self._create_temp_model_file(self.algorithm)
        self.model_info=self._driver_code(mlflow_experimemt_name)
        self._delete_temp_model_file()
        print(self.model_info)

    def _infer_signature(self, data):
        if self.algorithm=="PC":
            pc=PC()
            input_example=data.head()
            pc.learn(input_example)
            output_example= pc.causal_matrix
            signature = mlflow.models.infer_signature(input_example,output_example)
            print(signature)

    def _create_temp_model_file(self,algorithm):
        if algorithm=="PC":
            file_content=scripts.get_pc_script()
        else:
            raise ValueError(f"Unsupported model: {algorithm}")
        
        file_name = self.model_script_path
        with open(file_name, "w") as file:
            file.write(file_content)

        print(f"Model file '{file_name}' created successfully.")
    
    def _driver_code(self, mlflow_experimemt_name= None):
        if mlflow_experimemt_name==None:
            mlflow_experimemt_name=f"causal_matrix_{self.algorithm}"
        
        mlflow.set_experiment(mlflow_experimemt_name)
        with mlflow.start_run():
            model_info = mlflow.pyfunc.log_model(
                artifact_path="model",  
                python_model=self.model_script_path,  
                signature=self.signature,  
                registered_model_name=self.registered_model_name  
            )
        return(model_info)

    def _delete_temp_model_file(self):
            file_name = self.model_script_path
            if os.path.exists(file_name):
                os.remove(file_name)
                print(f"Temporary file '{file_name}' deleted.")
            else:
                print(f"File '{file_name}' does not exist, cannot delete.")


    def plot_causal_graph(self,causal_matrix,column_names,figsize=(5, 5),node_color="tab:blue",edge_color="yellow",node_size=1000,edge_width=3,font_size=12,font_color="white",layout_seed=123):
        """
        Creates and plots a directed graph based on a causal matrix.

        Parameters:
        - causal_matrix: 2D array or adjacency matrix representing causal relationships.
        - column_names: List of column names corresponding to the nodes.
        - figsize: Tuple, size of the figure (default (5, 5)).
        - node_color: Color of the nodes (default "tab:blue").
        - edge_color: Color of the edges (default "yellow").
        - node_size: Size of the nodes (default 1000).
        - edge_width: Width of the edges (default 3).
        - font_size: Font size for labels (default 12).
        - font_color: Color of the node labels (default "white").
        - layout_seed: Random seed for layout consistency (default 123).
        """
        # Create the figure
        fig, _ = plt.subplots(figsize=figsize)
        fig.patch.set_alpha(0)  # Make the background transparent

        # Create the graph
        g = nx.DiGraph(causal_matrix)

        # Layout positions
        pos = nx.spring_layout(g, seed=layout_seed)

        # Draw the graph
        nx.draw(
            G=g,
            pos=pos,
            node_color=node_color,
            edge_color=edge_color,
            node_size=node_size,
            width=edge_width,
        )

        # Draw labels
        labels = {i: column_names[i] for i in range(len(column_names))}
        nx.draw_networkx_labels(
            g, pos, labels=labels, font_size=font_size, font_color=font_color
        )

        # Show the plot
        #plt.show()
