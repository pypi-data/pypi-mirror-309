from django.db.models.signals import pre_save
from django.dispatch import receiver
from dcim.models import Device
from virtualization.models import VirtualMachine
from django.conf import settings
import re

def generate_next_name(prefix, existing_objects, exceptions=None):
    """
    Helper function to generate the next available name for a given prefix
    
    Handles number overflow by automatically adjusting padding length when needed.
    """
    used_numbers = set()
    
    # Add exceptions to used numbers if provided
    if exceptions:
        used_numbers.update(exceptions)
    
    # Get all used numbers from existing objects
    max_digits = 4  # Start with default 4 digits
    for obj in existing_objects:
        if obj.name is None:
            continue
        # Updated pattern to capture numbers of any length
        match = re.match(f'^{prefix}(\d+)$', obj.name)
        if match:
            num = int(match.group(1))
            used_numbers.add(num)
            # Track the maximum number of digits needed
            max_digits = max(max_digits, len(str(num)))
    
    if not used_numbers:
        return f"{prefix}0001"
    
    # Find the next available number
    current_num = 1
    while current_num in used_numbers:
        current_num += 1
        
    # Calculate required padding based on the number
    required_digits = max(max_digits, len(str(current_num)))
    
    # Format with required number of digits
    return f"{prefix}{current_num:0{required_digits}d}"

@receiver(pre_save, sender=Device)
def auto_generate_device_name(sender, instance, **kwargs):
    try:
        if not instance.name:
            role = instance.role.slug
            config = settings.PLUGINS_CONFIG['netbox_autonames']
            device_map = config.get('DEVICE_NAME_MAP', {})
            
            if role in device_map:
                role_config = device_map[role]
                if isinstance(role_config, str):
                    # Backwards compatibility for old config format
                    prefix = role_config
                    exceptions = []
                else:
                    prefix = role_config['prefix']
                    exceptions = role_config.get('exceptions', [])
                
                existing_devices = Device.objects.filter(role__slug=role)
                instance.name = generate_next_name(prefix, existing_devices, exceptions)
    except Exception as e:
        pass

@receiver(pre_save, sender=VirtualMachine)
def auto_generate_vm_name(sender, instance, **kwargs):
    try:
        if not instance.name:
            config = settings.PLUGINS_CONFIG['netbox_autonames']
            prefix = config.get('VM_PREFIX', 'VM')
            exceptions = config.get('VM_EXCEPTIONS', [])
            
            existing_vms = VirtualMachine.objects.all()
            instance.name = generate_next_name(prefix, existing_vms, exceptions)
    except Exception as e:
        pass