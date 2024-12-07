import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "alma-cdk.project",
    "version": "1.0.0.b11",
    "description": "Opinionated CDK Project “Framework”",
    "license": "Apache-2.0",
    "url": "https://github.com/alma-cdk/project.git",
    "long_description_content_type": "text/markdown",
    "author": "Alma Media<opensource@almamedia.dev>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/alma-cdk/project.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "alma_cdk.project",
        "alma_cdk.project._jsii"
    ],
    "package_data": {
        "alma_cdk.project._jsii": [
            "project@1.0.0-beta.11.jsii.tgz"
        ],
        "alma_cdk.project": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.133.0, <3.0.0",
        "constructs>=10.3.0, <11.0.0",
        "jsii>=1.105.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard>=2.13.3,<4.3.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
