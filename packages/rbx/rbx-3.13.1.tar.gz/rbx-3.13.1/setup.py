# Copyright 2022 Rockabox Media Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import find_packages, setup

AUTH = ["google-cloud-firestore>=2.3,<3"]
NOTIFICATIONS = [
    "google-cloud-pubsub>=2.9,<3",
]
QUEUES = [
    "redis<5",
    "hiredis>=3.0.0",
    "rq==1.10.1",
    "rq-scheduler==0.11.0",
]
STORAGE = ["google-cloud-storage>=2.1,<3"]
TASKS = ["google-cloud-tasks>=2.7,<3"]
WEB = ["google-cloud-error-reporting>=1.9.2,<2"]


setup(
    name="rbx",
    version="3.13.1",
    license="Apache 2.0",
    description="Scoota Platform utilities",
    long_description="A collection of common tools for Scoota services.",
    url="http://scoota.com/",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Internet",
    ],
    author="The Scoota Engineering Team",
    author_email="engineering@scoota.com",
    python_requires=">=3.9",
    install_requires=[
        "arrow>=1,<2",
        "cachetools>=4.2.4,<6",
        "Click<9",
        "colorama",
        "lxml>=5.3.0,<6",
        "requests>=2.31.0",
    ],
    extras_require={
        # These are requirement bundles required for specific feature sets.
        "auth": AUTH,
        "buildtools": [
            "bump-my-version",
            "check-manifest",
            "fabric~=3.2.0",
            "Jinja2==3.1.2",
            "twine",
        ],
        "notifications": NOTIFICATIONS,
        "platform": AUTH + NOTIFICATIONS + QUEUES + STORAGE,
        "queues": QUEUES,
        "storage": STORAGE,
        "tasks": TASKS,
        "web": WEB,
        # Include them all for the test suite.
        "test": AUTH + NOTIFICATIONS + QUEUES + STORAGE + TASKS + WEB,
    },
    entry_points={
        "console_scripts": [
            "buildtools = rbx.buildtools.cli:program.run [buildtools]",
        ],
    },
    packages=find_packages(),
)
