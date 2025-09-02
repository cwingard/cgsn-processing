# NSF Ocean Observatories Initiative (OOI) Mooring Data Processing

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python modules and shell scripts used to process the raw data files that were earlier parsed into JSON files via 
the [cgsn-parsers](https://bitbucket.org/ooicgsn/cgsn-parsers/src/master/) code. The processed data (calibration 
coefficients downloaded and applied, derived variables calculated, metadata added, etc.) is saved in NetCDF files that 
are then loaded into an [ERDDAP](https://coastwatch.pfeg.noaa.gov/erddap/index.html) data server used internally by 
the operations teams at [Oregon State University](https://oregonstate.edu) (managing the uncabled elements of the 
[Coastal Endurance Array](https://oceanobservatories.org/research-arrays/)) and [Woods Hole Oceanographic 
Institution](https://www.whoi.edu/) (managing the [Coastal Pioneer and Global Irminger and Station Papa 
arrays](https://oceanobservatories.org/research-arrays/)) to monitor the system health of the moorings and current 
environmental conditions.

This code is provided "as-is" for other users who may wish to process the data they have collected and parsed from the 
OOI moorings and load it into their own [ERDDAP](https://coastwatch.pfeg.noaa.gov/erddap/index.html) data server or 
other data processing system.

# Directory Organization
The python code for this project is available in the cgsn-processing/process directory.

Examples for how to work with some of the processors are presented in the notebooks directory using
[Jupyter](http://jupyter.org/) notebooks.

Different shell scripts in the utilities directory are presented both as examples of how to process data from the 
different instrument systems installed on a mooring (either individually or via a batch processing script) and as 
the actual scripts used by the operations teams to process the data (see the `processors` and `templates` folders). 
These scripts set the input and output directories for the data and call the appropriate python processor (located 
in the cgsn-processing/process directory) to use with that instrument. It should be noted that these scripts were 
created with a specific user and system in mind. Others will need to adapt these scripts to fit their own needs.

# Requirements
This code was written and tested against Python 3.12 using miniforge from [Conda-Forge](https://conda-forge.org/download/) 
community. The code has been used on Windows machines, as well as Linux servers running AlmaLinux 9 and Ubuntu 22.04.

The following python packages are used by this code:

* numpy
* scipy
* munch
* gsw
* beautifulsoup4
* pandas
* ppigrf
* netCDF4
* jinja2
* pytz
* requests
* xarray

# Contributing
Users are encouraged to contribute to this code. The hope is this repository can provide the science community with a 
means of accessing and working with the OOI mooring data. This project uses a [Forking 
Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/forking-workflow). To contribute, please fork 
the main [repo](https://bitbucket.org/ooicgsn/cgsn-process) to your own BitBucket account, create a branch, do your 
work, and then (when satisfied) submit a pull request to have your work integrated back into the main project repo 
(see a command line example of the workflow below).

This project uses [Semantic Versioning](https://semver.org/) with Major:Minor:Patch levels designated in the VERSION
file. Be sure to include/update the version level as appropriate based on the guidelines for Semantic Versioning and
provide that information in the pull request so the project admin can appropriately tag the code for automated builds
and testing.

An example work flow would be:
```bash
# A command workflow template for working with the OOI CGSN Parsers repository.

# Create your development directories (just a guide, use your own directories)
mkdir -p ~/dev/code
cd ~/dev/code

# Fork the ooicgsn/cgsn-processing repository to your account and clone a copy 
# of your fork to your development machine.
git clone git@bitbucket.org:<your_account>/cgsn-processing.git
 
# The next steps must be completed in the local repository directory
cd cgsn-processing
 
# Add the upstream feed for the master repository
git remote add upstream git@bitbucket.org:ooicgsn/cgsn-process.git
git fetch upstream

# Set the local master to point instead to the upstream master branch
git branch master --set-upstream-to upstream/master

# Keep your master branch updated, tied to the upstream master, and
# keep your remote fork in sync with the official repository (do this
# regularly)
git pull --ff-only upstream master
git push origin master

# Create your feature branch based off of the most recent version of the master
# branch by starting a new branch via...
#    git checkout master
#    git pull
#    git push origin master
# ... and then:
git checkout -b <branch>

### --- All of the next steps assume you are working in your <branch> --- ###
# Do your work, making incremental commits as/if needed, and back up to your
# bitbucket repository as/if needed.
while working == true
    git add <files>
    git commit -am "Commit Message"
    git push origin <branch>
end

# Before pushing your final changes to your repository, rebase your changes
# onto the latest code available from the upstream master.
git fetch upstream
git rebase -p upstream/master

# At this point you will need to deal with any conflicts, of which there should
# be none. Hopefully...

# Push the current working, rebased branch to your bitbucket fork and then 
# make a pull request to merge your work into the main code branch. Once the
# pull request is generated, add a comment with the following text:
#
#    @<code_admin> Ready for review and merge
#
# This will alert the main code admin to process the pull request.
git push -f origin <branch>
 
# At this point you can switch back to your master branch. Once the pull
# request has been merged into the main code repository, you can delete
# your working branches both on your local machine and from your bitbucket
# repository.
git checkout master
git pull
git push origin master
git branch -D <branch>
git branch -D origin/<branch>
```
