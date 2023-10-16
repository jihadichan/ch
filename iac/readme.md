# Run playbook

- Check provider for firewall config if IP still matches
- Server runs with password: ss, SSH key couldn't be added for some reason

```
ansible-playbook -i 123.123.123.123, playbook.yml --user root --ask-pass -e azure_key=XXXXXXXXXXX
```

