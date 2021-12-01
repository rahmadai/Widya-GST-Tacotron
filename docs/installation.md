## Getting started
### Clone Repository
First, you need to clone the repository to get all resources needs to use inference audio or even train a new model. We recommend you to use Linux because we haven't tested this project in Windows or Mac.

- Clone
    ```sh
    $ git clone https://github.com/ilhamfzri/Widya-GST-Tacotron.git
    ```

### Install Miniconda
If you are working on another project in your OS, we recommend you use miniconda to isolate the environment for this project because we use some specific package version and python version in this TTS. If you already have miniconda installed you can skip this step.

You can check this link to install miniconda
- [Tutorial Install Miniconda](https://docs.conda.io/en/latest/miniconda.html)

### Create and Activate New Miniconda Environment
As mentioned before we use a specific python version, so you need to create a new miniconda environment using python 3.7 :
- Create new environment
    ```sh
    $ conda create --name <your-env-name> python=3.7
    ```
After that you need to activate your new environment
- Activate new environment
    ```sh
    $ conda activate <your-env-name>
    ```

### Install Package & Dependencies
We use a lot of packages and dependencies to get this project works, thanks to the incredible open source community. To install all packages and dependencies needs, you can follow this step.

- Install packages & dependencies
    ```sh
    $ cd Widya-GST-Tacotron
    $ pip install -r requirement.txt
    ```
