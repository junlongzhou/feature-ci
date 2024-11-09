# Feature CI
Feature CI is a feature development and project management tool for Git based projects.


## Objective
Feature CI makes developers easier by showing changes in a side-by-side display, and allowing publish changes to next stage.

Feature CI simplifies Git based project maintainership by permitting any authorized user to submit changes to the master Git repository, rather than requiring all approved changes to be merged in by hand by the project maintainer.


## Documentation
For information about how to install and use FeatureCI, refer to [the documentation]().


## Source
Our canonical Git repository is located on [Github](https://github.com/junlongzhou/feature-ci).


## Reporting bugs
Please report bugs on the [issue tracker]().


## Contribute
Feature CI is the work of hundreds of contributors. We appreciate your help!

Please read the contribution [guidelines]().


## Getting in contact
The Developer Mailing list is repo-discuss on [FCI Groups]().

## License
Feature CI is provided under the Apache License 2.0.


## Build
```commandline
make
```

### Try aliyun mirror when you meet firewall issue
```
make -e ALPINE_MIRROR=https://mirrors.aliyun.com -e PYPI_INDEX=https://mirrors.aliyun.com/pypi/simple
```


## Run
```commandline
make deploy
```
