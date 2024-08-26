# Run playbook

- Check provider for firewall config if IP still matches

- Server runs with password: ss, SSH key couldn't be added for some reason

  ```bash
  ansible-playbook -i 123.123.123.123, playbook.yml --user root --ask-pass -e azure_key=XXXXXXXXXXX
  ```

  



# Renewing the SSL cert

- Certs needs to be renewed every 90 days. Can't be changed.

- You need to turn off the firewall before renewal. Afterwards, run:

  ```bash
  sudo certbot renew
  ```

  
