# Installation notes

These notes install a local Python3 instance using `miniconda`, then the 
`locust` package is installed by `pip`.

1. Clone the repository:

```
git clone https://github.com/glamod/glamod-wfs-benchmarker
```

2. Enter the directory:

```
cd glamod-wfs-benchmarker/
```

3. Download the miniconda installer and run it in batch mode:

``` 
wget https://repo.continuum.io/miniconda/Miniconda3-4.6.14-Linux-x86_64.sh
chmod 750 ./Miniconda3-4.6.14-Linux-x86_64.sh

./Miniconda3-4.6.14-Linux-x86_64.sh -b -p /home/users/astephen/glamod/glamod-wfs-benchmarker/miniconda3
```

4. Activate the base python3.7 conda environment:

```
export PATH=$PWD/miniconda3/bin:$PATH
source activate
```

5. Install locust:

```
pip install locust
```

6. Test it runs:

```
locust -h
```

7. Create a setup script:

```
echo cd $PWD > setup_env.sh
echo export PATH=\$PWD/miniconda3/bin:\$PATH >> setup_env.sh
echo source activate >> setup_env.sh
```

