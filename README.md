# Certificate Generator Server

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/06bd6acff9cd4506985192596642ef5f)](https://www.codacy.com/app/JBossOutreach/certificate-generator-server?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=JBossOutreach/certificate-generator-server&amp;utm_campaign=Badge_Grade)
[![Build Status](https://travis-ci.org/JBossOutreach/certificate-generator-server.svg?branch=master)](https://travis-ci.org/JBossOutreach/certificate-generator-server)
[![Gitter](https://img.shields.io/gitter/room/JBossOutreach/certificate-generator.svg)](https://gitter.im/JBossOutreach/certificate-generator)

An automatic certificate generator for events according to multiple input files like csv, xlsx, numbers and shoots emails with generated certificates.

## Setting up environment

- Install pipenv

```sh
pip install pipenv
```

- Create a pipenv

```sh
pipenv shell
```

As soon as the shell is ready,

- Run the following command to install the dependencies

```sh
pipenv install
```

The above command will install all of the dependencies.

- Set up environmental variables using:

```sh
cp .env.sample .env
```

Now edit .env and fill the generated `.env` file with your credentials to run it locally.

## Database 

For the Database to be used(in Production),
you can export the connection url in `DATABASE_URL`,
eg,
```sh
$ export DATABASE_URL=postgres://postgres:mysecretpassword@127.0.0.1:5432/test
```

## Running

```sh
python manage.py makemigrations api
python manage.py migrate
python manage.py runserver
```

To stop the server, press `Ctrl + C` and deactivate the virtual environment using `deactivate` command.

## Running in docker
1.  Build image
```sh
sudo docker build . -t cert-gen-server:latest
```
2.  Run container
```sh
sudo docker run -d --name cert-gen cert-gen-server:latest
```
3.  If you want to add packages, you would need to get a shell as root:
```sh
sudo docker exec --it --user root cert-gen sh

# In docker container
apk add curl
```
## Post setup instructions

Instead of adding new dependencies to requirements.txt, simply run:

```sh
pipenv install <package-name>
```

to install it inside pipenv and add it to Pipfile.

To lock the dependencies for deployment, run:

```sh
pipenv lock
```

## Setting up project
 
 **1.** **Fork** this project by clicking the _Fork_ button on top right corner of this page.
 
 **2.** **Clone** the repository by running following command in [git](https://git-scm.com/):
 ```sh
 $ git clone https://github.com/[YOUR-USERNAME]/certificate-generator-server.git
 ```
 
 ## Contributing
 
 **1.** Make reasonable changes.
 
 **2.** **Add all changes** by running this command on the terminal/command prompt:
 ```sh
 $ git add .
 ```
 Or to add specific files only, run this command:
 ```sh
 $ git add path/to/your/file
 ```
 Make sure you replace `path/to/your/file` with the actual path to the file you want to add to the staging area.
 
 **3.** **Commit** changes.
 ```sh
 $ git commit -m "DESCRIBE YOUR CHANGES HERE"
 ```
 **4.** **Push** your changes.
 ```sh
 $ git push origin
 ```
 **5.** **Create a Pull Request** by clicking the _New pull request_ button on your repository page.
 
 **6.** Always Squash your commits when sending the Pull request
 
 **NOTE** Make sure that you include a desription of changes made by you.
 
 ## Help
 
 If you need any help anywhere in the process, you can always ask a question on our [Gitter Chat](https://gitter.im/jboss-outreach/gci).

## License

This project is currently licensed under the **[GNU General Public License v3](LICENSE.md)**.
i.e. we guarantee end users the freedom to run, study, share, and modify the software.

> To obtain the software under a different license, please contact [JBossOutreach](https://gitter.im/JBossOutreach/gci).
