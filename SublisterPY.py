import requests
import tldextract
import os

def get_subdomains(domain):
    """
    Fetches subdomains for the given domain using crt.sh.

    :param domain: The target domain (e.g., 'netflix.com')
    :return: A set of discovered subdomains
    """
    url = f"https://crt.sh/?q=%25.{domain}&output=json"

    try:
        response = requests.get(url, timeout=30)

        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code} from crt.sh")
            return set()

        try:
            data = response.json()
        except ValueError:
            print("Error: Unable to parse JSON response from crt.sh")
            return set()

        subdomains = set()

        for entry in data:
            if 'name_value' in entry:
                names = entry['name_value'].split('\n')
                for name in names:
                    subdomain = name.strip().lower()
                    if '*' not in subdomain and subdomain.endswith(domain):
                        subdomains.add(subdomain)

        return subdomains

    except requests.RequestException as e:
        print(f"Error: An exception occurred while querying crt.sh: {e}")
        return set()

def save_to_file(subdomains, domain):
    """
    Saves the discovered subdomains to a text file in the PYSITES folder on the desktop.

    :param subdomains: A set of discovered subdomains
    :param domain: The target domain (used for naming the output file)
    """
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    output_dir = os.path.join(desktop_path, "PYSITES")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = os.path.join(output_dir, f"{domain}_subdomains.txt")

    try:
        with open(output_file, 'w') as f:
            for subdomain in sorted(subdomains):
                f.write(subdomain + '\n')
        print(f"Subdomains saved to {output_file}")
    except IOError as e:
        print(f"Error: Unable to save subdomains to file: {e}")

def main():
    domain = input("Enter the domain (e.g., netflix.com): ").strip().lower()

    extracted = tldextract.extract(domain)
    registered_domain = f"{extracted.domain}.{extracted.suffix}"

    if not extracted.domain or not extracted.suffix:
        print("Error: Invalid domain format.")
        return

    subdomains = get_subdomains(registered_domain)

    if subdomains:
        print(f"\nSubdomains found for {registered_domain}:")
        for sub in sorted(subdomains):
            print(f"- {sub}")
        save_to_file(subdomains, registered_domain)
    else:
        print(f"No subdomains found for {registered_domain}.")

if __name__ == "__main__":
    main()
