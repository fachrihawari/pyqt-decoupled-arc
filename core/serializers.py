"""
Serializers for converting domain objects to dictionaries (DTOs).
This layer helps maintain clean separation between domain models and presentation.
"""

def contact_to_dict(contact):
    """
    Convert a Contact domain object to a dictionary representation.
    
    Args:
        contact: Contact domain object
        
    Returns:
        dict: Dictionary with contact data suitable for UI/API consumption
    """
    return {
        'id': contact.id,
        'name': contact.name,
        'email': contact.email,
        'phone': contact.phone
    }


def contacts_to_dict_list(contacts):
    """
    Convert a list of Contact domain objects to a list of dictionaries.
    
    Args:
        contacts: List of Contact domain objects
        
    Returns:
        list: List of dictionaries with contact data
    """
    return [contact_to_dict(contact) for contact in contacts]
