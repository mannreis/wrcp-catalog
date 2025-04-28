import yaml

def merge_catalogs(catalogs):
    """
    Merges multiple YAML catalogs into a single catalog.
    
    Args:
        catalogs (list): List of file paths to the YAML catalogs.
        Last in list wins.
    
    Returns:
        dict: Merged catalog.
    """
    merged_catalog = dict (sources = dict())
    
    for catalog in catalogs:
        with open(catalog, 'r') as file:
            data = yaml.safe_load(file)
            merged_catalog["sources"].update(data.get("sources", {}))
    return merged_catalog

def save_merged_catalog(merged_catalog, output_file):
    """
    Saves the merged catalog to a YAML file.
    
    Args:
        merged_catalog (dict): Merged catalog.
        output_file (str): Path to the output YAML file.
    """
    with open(output_file, 'w') as file:
        yaml.dump(merged_catalog, file, default_flow_style=False)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Merge multiple YAML catalogs into a single catalog.")
    parser.add_argument('catalogs', nargs='+', help='List of YAML catalog files to merge.')
    parser.add_argument('--output', default='merged_catalog.yaml', help='Output file for the merged catalog.')
    
    args = parser.parse_args()
    
    merged_catalog = merge_catalogs(args.catalogs)
    save_merged_catalog(merged_catalog, args.output)
    
    print(f"Merged catalog saved to {args.output}")
