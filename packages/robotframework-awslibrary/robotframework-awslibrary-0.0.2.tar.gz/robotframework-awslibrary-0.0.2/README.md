# robotframework-awslibrary

`robotframework-awslibrary` é uma biblioteca Python para criar casos de teste para serviços da AWS usando o Robot Framework.

## Instalação

Para instalar a biblioteca, você pode usar o `pip`:

```sh
pip install robotframework-awslibrary

```

## Requisitos
Python 3.10+

Robot Framework 7.1.1+
Boto3 1.35.62+
Robot Framework PythonLibCore 4.4.1+

## Uso
Para usar a biblioteca em seus testes do Robot Framework, você pode importar a biblioteca no seu arquivo .robot:

```robot
*** Settings ***
Library    AWSLibrary

*** Test Cases ***
Create a S3 bucket
    ${bucket_name}    S3 create bucket    test-robotframework-s3-bucket
    Should Be Equal As Strings    test-robotframework-s3-bucket    ${bucket_name}

Delete a S3 bucket
    S3 delete bucket    test-robotframework-s3-bucket

Verify a S3 bucket exists
    S3 create bucket    test-robotframework-s3-bucket
    S3 Should Exists    test-robotframework-s3-bucket
    S3 delete bucket    test-robotframework-s3-bucket

Put a Object in a S3 bucket
    S3 create bucket    test-robotframework-s3-bucket
    S3 put object    test-robotframework-s3-bucket    test-robotframework-s3-object
```

## Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## Licença
Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.