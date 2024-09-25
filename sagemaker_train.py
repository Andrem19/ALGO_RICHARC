import sagemaker
from sagemaker.tensorflow import TensorFlow

sagemaker_session = sagemaker.Session()
role = 'arn:aws:iam::778336162041:role/awsSageMakerRole'  # Замените на вашу роль IAM

estimator = TensorFlow(entry_point='train_2.py',
                       role=role,
                       instance_count=1,
                       instance_type='ml.g5.xlarge',
                       framework_version='2.3.0',
                       py_version='py37',
                       script_mode=True,
                       hyperparameters={
                           'file-path': 's3://sagemodels1/data/train_data.csv',
                           'n-steps': 84,
                           'epochs': 1000,
                           'batch-size': 32
                       },
                       dependencies=['requirements.txt'])

estimator.fit({'train': 's3://sagemodels1/data/train_data.csv'})
