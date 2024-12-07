# !/usr/bin/python3
# -*- encoding: utf-8 -*-
# author: zsp

import pandas as pd
import pickle
import numpy as np
import joblib
import warnings
warnings.filterwarnings('ignore')
import mlflow
import logging
logging.getLogger("mlflow").setLevel(logging.ERROR)
from mlflow.models.signature import infer_signature
from mlflow.pyfunc import load_model
import numpy as np
import pandas as pd
import pickle
import os
import sys
import inspect
import tempfile
import yaml
from packaging import version

def parse_package(pkg):
    if "==" in pkg:
        pkg_name, pkg_version = pkg.split("==")
    else:
        pkg_name = pkg
        pkg_version = None
    return pkg_name, pkg_version
    
def merge_pip_requirements(original, extra):
    merged = {}
    for req in original:
        pkg_name, pkg_version = parse_package(req)
        merged[pkg_name] = pkg_version
    # Add/Update with extra requirements
    for req in extra:
        pkg_name, pkg_version = parse_package(req)
        if pkg_name in merged:
            if pkg_version and (merged[pkg_name] is None or version.parse(pkg_version) > version.parse(merged[pkg_name])):
                merged[pkg_name] = pkg_version
        else:
            merged[pkg_name] = pkg_version
    # Reconstruct the pip requirements list
    merged_requirements = []
    for pkg_name, pkg_version in merged.items():
        if pkg_version:
            merged_requirements.append(f"{pkg_name}=={pkg_version}")
        else:
            merged_requirements.append(pkg_name)
    return merged_requirements

class ModelWrapper(mlflow.pyfunc.PythonModel):
    def __init__(self, pre_func, model, post_func, predict_method):
        super().__init__()
        self.pre_func = pre_func
        self.model = model
        self.post_func = post_func
        self.predict_method = predict_method

    def _call(self, dataframe):
        pre_data = self.pre_func(dataframe) if self.pre_func else dataframe
        if self.predict_method == "predict_proba":
            pred_raw = self.model.predict_proba(pre_data)[:, 1] if self.model else pre_data
        elif predict_method == "predict":
            pred_raw = self.model.predict(pre_data) if self.model else pre_data
        else:
            raise ValueError(f"The prediction method '{predict_method}' is not supported.")
        pred_end = self.post_func(pred_raw) if self.post_func else pred_raw
        return pred_end
        
def log_sklearn_model(experiment_name,data,model,pre_func,post_func,predict_method,extra_pip_requirements,env_name,input_signature=None):
    with mlflow.start_run(run_name=experiment_name) as run:
        print(run.info.artifact_uri)
        runid = run.info.run_id
        custom_model = ModelWrapper(pre_func, model, post_func, predict_method)
        with tempfile.TemporaryDirectory() as d:
            if pre_func:
                pre_func_path = os.path.join(d, 'pre_func.py')
                with open(pre_func_path, 'w') as f:
                    f.write(inspect.getsource(pre_func))
                mlflow.log_artifact(pre_func_path, 'pre_func')
            if post_func:
                post_func_path = os.path.join(d, 'post_func.py')
                with open(post_func_path, 'w') as f:
                    f.write(inspect.getsource(post_func))
                mlflow.log_artifact(post_func_path, 'post_func')
            data_path = d + '/data.csv'
            data.sample(1).to_csv(data_path,index=None)
            mlflow.log_artifact(data_path, 'data')
            model_path = os.path.join(d, 'model')
            extra_pip_requirements = extra_pip_requirements + ['docopt==0.6.2','snowpaw==0.0.3','oss2==2.19.1']
            mlflow.pyfunc.save_model(path=model_path,python_model=custom_model._call,extra_pip_requirements=extra_pip_requirements)
            temp_conda_yaml_path = os.path.join(model_path, 'conda.yaml')
            with open(temp_conda_yaml_path, 'r') as file:
                conda_env = yaml.safe_load(file)
            conda_env['name'] = env_name
            original_pip_requirements = []
            if 'pip' in conda_env['dependencies'][-1]:
                original_pip_requirements = conda_env['dependencies'][-1]['pip']
            merged_pip_requirements = merge_pip_requirements(original_pip_requirements, extra_pip_requirements)
            conda_env['dependencies'][-1]['pip'] = merged_pip_requirements
        pre_data = pre_func(data.sample(1)) if pre_func else data.sample(1)
        signature = infer_signature(pre_data)
        mlflow.pyfunc.log_model(artifact_path='func_model', python_model=custom_model._call, input_example=data,signature=signature, conda_env=conda_env)
    return runid

def log_func(experiment_name,data,pre_func,extra_pip_requirements,env_name,cols):
    with mlflow.start_run(run_name=experiment_name) as run:
        print(run.info.artifact_uri)
        runid = run.info.run_id
        with tempfile.TemporaryDirectory() as d:
            if pre_func:
                pre_func_path = os.path.join(d, 'pre_func.py')
                with open(pre_func_path, 'w') as f:
                    f.write(inspect.getsource(pre_func))
                mlflow.log_artifact(pre_func_path, 'pre_func')
            data_path = d + '/data.csv'
            data.sample(1).to_csv(data_path,index=None)
            mlflow.log_artifact(data_path, 'data')
            model_path = os.path.join(d, 'model')
            extra_pip_requirements = extra_pip_requirements + ['docopt==0.6.2','snowpaw==0.0.3','oss2==2.19.1']
            mlflow.pyfunc.save_model(path=model_path,python_model=pre_func,extra_pip_requirements=extra_pip_requirements)
            temp_conda_yaml_path = os.path.join(model_path, 'conda.yaml')
            with open(temp_conda_yaml_path, 'r') as file:
                conda_env = yaml.safe_load(file)
            conda_env['name'] = env_name
            original_pip_requirements = []
            if 'pip' in conda_env['dependencies'][-1]:
                original_pip_requirements = conda_env['dependencies'][-1]['pip']
            merged_pip_requirements = merge_pip_requirements(original_pip_requirements, extra_pip_requirements)
            conda_env['dependencies'][-1]['pip'] = merged_pip_requirements
        signature = infer_signature(data[cols])
        mlflow.pyfunc.log_model(artifact_path='func_model', python_model=pre_func, input_example=data,signature=signature, conda_env=conda_env)
    return runid

def mlflow_log(experiment_name,data,pre_func=None,model=None,model_type='sklearn',post_func=None,predict_method="predict_proba",extra_pip_requirements=[],uri=None,**kwargs):
    """
    params:
        model_type (str): 'sklearn', 'torch' ,'func'
    """
    active_run = mlflow.active_run()
    if active_run:
        mlflow.end_run()
    mlflow.set_tracking_uri(uri=uri)
    mlflow.create_experiment(experiment_name, artifact_location="oss://bigdata-mlflow/sh_models")
    mlflow.set_experiment(experiment_name)
    # 检查是否有活动的 run
    if pre_func is None and model is None:
        raise Exception('pre_func and model both none illegal input !!!')
    version = sys.version_info
    env_name='py'+str(version.major)+str(version.minor)+str(version.micro)
    if model_type =='sklearn':
        run_id = log_sklearn_model(experiment_name,data,model,pre_func,post_func,predict_method,extra_pip_requirements,env_name)
    elif model_type =='func':
        run_id = log_func(experiment_name,data,pre_func,extra_pip_requirements,env_name,cols=kwargs['cols'])
    else: # torch
        pass
    try:
        user_name = os.environ['JUPYTERHUB_USER']
    except:
        user_name = os.environ['USERNAME']
    tags = {'user_name': user_name,'python_version':'.'.join(map(str, sys.version_info[:3]))}
    mlflow.register_model(f'runs:/{run_id}/func_model',experiment_name,tags=tags)
    
    mlflow.end_run()
    return run_id

def mlflow_test(run_id,data):
    model_uri = f'oss://bigdata-mlflow/sh_models/{run_id}/artifacts/func_model'
    model = mlflow.pyfunc.load_model(model_uri)
    pred = model.predict(data)
    return pred

# cd 对应路径
# pip install -e .