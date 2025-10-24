import customtkinter as ctk

class AppTheme:
    """It defines global styles and themes for the application."""
    # Define color schemes
        # Cores de destaque e fundo
    PRIMARY_COLOR    = "#2B2B2B"
    SECONDARY_COLOR  = "#404040"
    ACCENT_COLOR     = "#0078D4"
    SUCCESS_COLOR    = "#107C10"
    WARNING_COLOR    = "#FF8C00"
    DANGER_COLOR     = "#D13438"
    
    BG_PRIMARY       = "#1E1E1E"
    BG_SECONDARY     = "#2D2D2D"
    BG_SURFACE       = "#3D3D3D"
    
    TEXT_PRIMARY     = "#FFFFFF"
    TEXT_SECONDARY   = "#CCCCCC"
    TEXT_MUTED       = "#999999"
    
    CORNER_RADIUS    = 8
    BORDER_WIDTH     = 1
    
    @classmethod
    def configure_appearance(cls):
        """Dark and light mode configuration"""
        ctk.set_appearance_mode("dark")  # Modos: "dark", "light"
        ctk.set_default_color_theme("dark-blue")  # Temas: "blue", "dark-blue", "green"
  
class ComponentStyles:
    """Returns standardized styles for GUI components."""
    
    @staticmethod
    def get_main_button():
        return {
            "corner_radius": AppTheme.CORNER_RADIUS,
            "height":        40,
            "font":          ("Segoe UI", 12, "bold"),
            "fg_color":      AppTheme.ACCENT_COLOR,
            "hover_color":   "#106EBE"
        }
    @staticmethod
    def get_danger_button():
        return {
            "corner_radius": AppTheme.CORNER_RADIUS,
            "height":        35,
            "font":          ("Segoe UI", 11),
            "fg_color":      AppTheme.DANGER_COLOR,
            "hover_color":   "#B02A2E"
        }
    
    @staticmethod
    def get_task_card():
        return {
            "corner_radius": AppTheme.CORNER_RADIUS,
            "fg_color":      AppTheme.BG_SURFACE,
            "border_width":  AppTheme.BORDER_WIDTH,
            "border_color":  AppTheme.SECONDARY_COLOR
        }