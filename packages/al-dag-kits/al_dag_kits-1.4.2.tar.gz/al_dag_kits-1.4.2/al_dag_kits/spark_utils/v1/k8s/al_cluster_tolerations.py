from enum import Enum

class ClusterSize(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    BIG = "big"

class ClusterType(Enum):
    DEDICATED = "dedicated"
    SPOT = "spot"

cluster_type_values = set(ctype.value for ctype in ClusterType)
cluster_size_values = set(size.value for size in ClusterSize)

def parse_tolerations(tolerations_input):
    """
    Parses the input list of tolerations and returns a list of toleration dictionaries
    based on the specified logic.

    Logic:
    1. If 'spot' is in the input, include 'spot=true' and exclude 'dedicated=true'.
    2. If no ClusterType is specified, default to 'dedicated=true'.
    3. If specific sizes are provided, include only those sizes.
       Else, include all sizes.
    4. For any unknown tolerations, include them with 'value' set to 'true'.

    Args:
        tolerations_input (list of str): List containing cluster types, sizes, and/or unknown tolerations.

    Returns:
        list of dict: List of toleration dictionaries.
    """
    cluster_types = set()
    cluster_sizes = set()
    unknown_tolerations = set()
    
    for toleration in tolerations_input:
        if toleration in cluster_type_values:
            cluster_types.add(toleration)

        elif toleration in cluster_size_values:
            cluster_sizes.add(toleration)
        
        else:
            unknown_tolerations.add(toleration)
    
    result = []
    
    # Handle Cluster Types
    if 'spot' in cluster_types:
        # If 'spot' is present, include 'spot=true' and exclude 'dedicated=true'
        result.append({
            "effect": "NoSchedule",
            "key": "spot",
            "value": "true"
        })
    elif not cluster_types:
        # If no ClusterType is specified, default to 'dedicated=true'
        result.append({
            "effect": "NoSchedule",
            "key": "dedicated",
            "value": "true"
        })
    else:
        # Include all specified ClusterTypes except 'spot' (already handled)
        for ctype in cluster_types:
            result.append({
                "effect": "NoSchedule",
                "key": ctype,
                "value": "true"
            })
    
    # Handle Cluster Sizes
    if cluster_sizes:
        # If specific sizes are provided, include them
        for size in cluster_sizes:
            result.append({
                "effect": "NoSchedule",
                "key": "size",
                "value": size
            })
    else:
        # If no sizes are specified, include all sizes
        for size in ClusterSize:
            result.append({
                "effect": "NoSchedule",
                "key": "size",
                "value": size.value
            })
    
    if unknown_tolerations:
        # Handle Unknown Tolerations
        for key in [*unknown_tolerations, *cluster_types]:
            result = [{
                "effect": "NoSchedule",
                "key": key,
                "value": "true"
            }]
        for size in cluster_sizes:
            result.append({
                "effect": "NoSchedule",
                "key": "size",
                "value": size
            })
    
    return result
