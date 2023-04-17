from enum import Enum

class RoleChoice(Enum):   # A subclass of Enum
  SUPERADMIN = "Superadmin"
  ADMIN = "Admin"
  ASSISTANT = "Assistant"
  SUPPORT = "Support"
  RETURN_CUSTOMER = "Returning Customer"
  CUSTOMER = "Customer"
  REGISTER_USER = "Registered User"
  USER = "User"
  AFFILIATE = "Affiliate"
  def __str__(self):
    return self.value
class StatusChoice(Enum):   # A subclass of Enum
  PENDING = "Pending"
  ALLOWED = "Allowed"
  DISALLOWED = "Disallowed"
  DELETED = "Deleted"
  def __str__(self):
    return self.value
  