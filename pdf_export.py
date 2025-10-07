"""
PDF Export Module
Generates professional PDF reports from course data
"""

from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
from typing import List, Dict
import os


class PDFExporter:
    """Generates PDF reports from course data"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#3B82F6'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#6B7280'),
            spaceAfter=12,
            alignment=TA_LEFT,
            fontName='Helvetica'
        ))
    
    def export_to_pdf(self, courses: List[Dict], user_id: str, filename: str = None) -> str:
        """
        Export course data to PDF
        
        Args:
            courses: List of course dictionaries
            user_id: Student ID
            filename: Optional custom filename
            
        Returns:
            Path to generated PDF file
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            filename = f'EWU_Courses_{timestamp}.pdf'
        
        # Ensure .pdf extension
        if not filename.endswith('.pdf'):
            filename += '.pdf'
        
        # Ensure output directory exists
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)
        
        # Full path to PDF file
        filepath = os.path.join(output_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=landscape(A4),
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Container for PDF elements
        elements = []
        
        # Title
        title = Paragraph("EWU Course Schedule", self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))
        
        # User info
        current_time = datetime.now().strftime('%b %d, %Y %I:%M %p')
        user_info = Paragraph(f"Student ID: {user_id}", self.styles['CustomSubtitle'])
        date_info = Paragraph(f"Generated: {current_time}", self.styles['CustomSubtitle'])
        elements.append(user_info)
        elements.append(date_info)
        elements.append(Spacer(1, 0.3*inch))
        
        # Prepare table data
        table_data = [['Course Code', 'Section', 'Faculty', 'Capacity', 'Taken', 'Available', 'Day', 'Time', 'Room']]
        
        for course in courses:
            available = course.get('SeatCapacity', 0) - course.get('SeatTaken', 0)
            day_time = self._parse_day_time(course.get('TimeSlotName', ''))
            
            row = [
                course.get('CourseCode', 'N/A'),
                course.get('SectionName', 'N/A'),
                course.get('ShortName', 'N/A'),
                str(course.get('SeatCapacity', 0)),
                str(course.get('SeatTaken', 0)),
                str(available),
                day_time['day'],
                day_time['time'],
                course.get('RoomName', 'N/A')
            ]
            table_data.append(row)
        
        # Create table
        table = Table(table_data, colWidths=[
            1.0*inch,  # Course Code
            0.7*inch,  # Section
            1.4*inch,  # Faculty
            0.8*inch,  # Capacity
            0.7*inch,  # Taken
            0.8*inch,  # Available
            1.4*inch,  # Day
            1.2*inch,  # Time
            0.9*inch   # Room
        ])
        
        # Style the table
        table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3B82F6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            
            # Body
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('ALIGN', (3, 1), (5, -1), 'CENTER'),  # Center align capacity, taken, available
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#3B82F6')),
            
            # Alternating row colors
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F7FA')])
        ]))
        
        elements.append(table)
        
        # Build PDF
        doc.build(elements)
        
        return os.path.abspath(filepath)
    
    @staticmethod
    def _parse_day_time(time_slot_name: str) -> Dict[str, str]:
        """Parse day and time from TimeSlotName"""
        if not time_slot_name:
            return {'day': '', 'time': ''}
        
        day_mapping = {
            'A': 'SATURDAY',
            'S': 'SUNDAY',
            'M': 'MONDAY',
            'T': 'TUESDAY',
            'W': 'WEDNESDAY',
            'R': 'THURSDAY'
        }
        
        import re
        day_match = re.match(r'^[ASMTWR]+', time_slot_name)
        day_abbr = day_match.group(0) if day_match else ''
        day_names = ', '.join([day_mapping.get(d, d) for d in day_abbr])
        time = re.sub(r'^[ASMTWR]+\s*', '', time_slot_name).strip()
        
        return {'day': day_names, 'time': time}

