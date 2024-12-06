class NameManager:
    def _format_library_name(self, lib_name: str) -> str:
        """Format a library name for use as a pod name.
        Args:
            lib_name (str): Name of the library.
            
        Returns:
            str: Formatted library name.
        """
        formatted_name = "".join(
            c if c.isalnum() or c in "-._" else "_" for c in lib_name
        )
        while "__" in formatted_name:
            formatted_name = formatted_name.replace("__", "_").lower()
        return formatted_name
    
    def _pod_lib_name(self, pod_name: str) -> str:
        """Generate a library name from a pod name.
        Args:
            pod_name (str): Name of the pod.
            
        Returns:
            str: Library name.
        """
        return f"{pod_name}_lib"
        