# gitlab grabber

install via pypi
```bash
pip install gitlab-grabber
```

man
```bash
gitlab_grabber --help
```

Usage to clone all repo via http (oauth)
```bash
gitlab_grabber -t <token> -u <domain> -k -d /<dir> --auth http
```

Usage to clone all repo via ssh
```bash
gitlab_grabber -t <token> -u <domain> -k -d /<dir> -i <path_to_ssh_private_key>
```

Clone via ssh is default. 
**-k** - skip SSL verify
**-crt-path** - path to CA certificate.
**-d** - clone dir. Default is dir when tool is will run.