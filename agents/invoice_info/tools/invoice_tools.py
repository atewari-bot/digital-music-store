from langchain_core.tools import tool
from da.db import get_chinook_db
import logging

@tool
def get_invoices_by_customer_sorted_by_date(customer_id: str) -> list[dict]:
    """
    Returns a list of invoices for a specific customer, sorted by date in descending order.
    
    Args:
        customer_id (str): The ID of the customer whose invoices are to be retrieved.
        
    Returns:
        list[dict]: A list of invoices for the customer sorted by date.
    """
    try:
        if not customer_id or not customer_id.strip():
            return [{"error": "Customer ID cannot be empty"}]
        
        # Validate customer_id is numeric
        try:
            int(customer_id)
        except ValueError:
            return [{"error": f"Invalid customer ID format: {customer_id}"}]

        result = get_chinook_db().run(
            f"""
            SELECT *
            FROM Invoice
            WHERE Invoice.CustomerId = '{customer_id}'
            ORDER BY Invoice.InvoiceDate DESC;
            """,
            include_columns=True,
        )
        
        return result if result else [{"message": f"No invoices found for customer {customer_id}"}]
    except Exception as e:
        logging.error(f"Error in get_invoices_by_customer_sorted_by_date: {e}")
        return [{"error": f"Error retrieving invoices for customer {customer_id}: {str(e)}"}]

@tool
def get_invoices_sorted_by_unit_price(customer_id: str) -> list[dict]:
    """
    Returns a list of invoices for a specific customer sorted by unit price in descending order.
    
    Args:
        customer_id (str): The ID of the customer whose invoices are to be retrieved.
        
    Returns:
        list[dict]: A list of invoices sorted by unit price.
    """
    try:
        if not customer_id or not customer_id.strip():
            return [{"error": "Customer ID cannot be empty"}]
        
        # Validate customer_id is numeric
        try:
            int(customer_id)
        except ValueError:
            return [{"error": f"Invalid customer ID format: {customer_id}"}]

        result = get_chinook_db().run(
            f"""
            SELECT Invoice.*, InvoiceLine.UnitPrice
            FROM Invoice
            JOIN InvoiceLine ON Invoice.InvoiceId = InvoiceLine.InvoiceId
            WHERE Invoice.CustomerId = '{customer_id}'
            ORDER BY InvoiceLine.UnitPrice DESC;
            """,
            include_columns=True,
        )
        
        return result if result else [{"message": f"No invoices found for customer {customer_id}"}]
    except Exception as e:
        logging.error(f"Error in get_invoices_sorted_by_unit_price: {e}")
        return [{"error": f"Error retrieving invoices for customer {customer_id}: {str(e)}"}]

@tool
def get_employee_by_invoice_and_customer(invoice_id: str, customer_id: str) -> list[dict]:
    """
    Returns employee information for a specific invoice and customer.
    
    Args:
        invoice_id (str): The ID of the invoice associated with the employee.
        customer_id (str): The ID of the customer whose invoices are to be retrieved.
        
    Returns:
        list[dict]: Employee information for the specified invoice and customer.
    """
    try:
        if not invoice_id or not invoice_id.strip():
            return [{"error": "Invoice ID cannot be empty"}]
        if not customer_id or not customer_id.strip():
            return [{"error": "Customer ID cannot be empty"}]
        
        # Validate IDs are numeric
        try:
            int(invoice_id)
            int(customer_id)
        except ValueError:
            return [{"error": f"Invalid ID format: invoice_id={invoice_id}, customer_id={customer_id}"}]
        
        query = f"""
            SELECT Employee.FirstName, Employee.Title, Employee.Email
            FROM Employee
            JOIN Customer ON Customer.SupportRepId = Employee.EmployeeId
            JOIN Invoice ON Invoice.CustomerId = Customer.CustomerId
            WHERE Invoice.InvoiceId = '{invoice_id}' AND Invoice.CustomerId = '{customer_id}';
            """
        employee_info = get_chinook_db().run(
            query,
            include_columns=True
        )

        if not employee_info:
            return [{"message": f"No employee found for invoice {invoice_id} and customer {customer_id}."}]
        return employee_info if isinstance(employee_info, list) else [employee_info]
    except Exception as e:
        logging.error(f"Error in get_employee_by_invoice_and_customer: {e}")
        return [{"error": f"Error retrieving employee info: {str(e)}"}]

def get_invoice_tools():
    """
    Returns a list of tools related to invoice management.
    
    This function provides access to various tools that can be used to manage and retrieve invoice information.
    
    Returns:
        list: A list of tools for invoice management.
    """
    return [
        get_invoices_by_customer_sorted_by_date,
        get_invoices_sorted_by_unit_price,
        get_employee_by_invoice_and_customer
    ]