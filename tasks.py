from invoke import task
from pathlib import Path
import os
import os.path
import shutil
import glob


@task
def robot(ctx):
    ctx.run("robot -A atest/run_tests.robot")


@task
def up(ctx):
    ctx.run("docker-compose up -d")


@task
def down(ctx):
    ctx.run("docker-compose down")


@task
def build(ctx):
    ctx.run("docker-compose up --build")


@task
def prune(ctx):
    ctx.run("docker system prune --all")


@task
def clean(ctx):
    to_be_removed = [
        "coverage_report/",
        "reports/",
        "src/robotframework_seleniumtestability.egg-info/",
        "dist/",
        "output.xml",
        ".coveragedb",
        "*.html",
        "selenium-screenshot-*.png",
        "geckodriver.log",
        "SeleniumProxy.log",
    ]

    for item in to_be_removed:
        if os.path.isdir(item):
            shutil.rmtree(item)
        elif os.path.isfile(item):
            os.remove(item)
        else:
            for filename in glob.glob(item):
                os.remove(filename)
