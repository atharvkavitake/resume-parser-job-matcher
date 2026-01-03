import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';

export const generateATSReportPDF = (atsData, resumeName) => {
  const doc = new jsPDF();
  const pageWidth = doc.internal.pageSize.getWidth();
  const pageHeight = doc.internal.pageSize.getHeight();
  let yPosition = 20;

  // Header
  doc.setFillColor(102, 126, 234);
  doc.rect(0, 0, pageWidth, 40, 'F');
  
  doc.setTextColor(255, 255, 255);
  doc.setFontSize(24);
  doc.setFont('helvetica', 'bold');
  doc.text('ATS Score Report', pageWidth / 2, 20, { align: 'center' });
  
  doc.setFontSize(12);
  doc.setFont('helvetica', 'normal');
  doc.text(`Candidate: ${resumeName}`, pageWidth / 2, 30, { align: 'center' });
  doc.text(`Generated: ${new Date().toLocaleDateString()}`, pageWidth / 2, 36, { align: 'center' });

  yPosition = 50;

  // Overall Score Section
  doc.setTextColor(0, 0, 0);
  doc.setFontSize(18);
  doc.setFont('helvetica', 'bold');
  doc.text('Overall ATS Score', 20, yPosition);
  
  yPosition += 10;
  doc.setFontSize(48);
  doc.setTextColor(102, 126, 234);
  doc.text(`${atsData.ats_score}%`, 20, yPosition);
  
  yPosition += 8;
  doc.setFontSize(14);
  doc.setTextColor(0, 0, 0);
  doc.setFont('helvetica', 'normal');
  doc.text(`Grade: ${atsData.grade} | Rating: ${atsData.rating}`, 20, yPosition);
  
  yPosition += 15;

  // Verdict
  const verdict = getVerdictText(atsData.ats_score);
  doc.setFontSize(12);
  doc.setTextColor(100, 100, 100);
  doc.text(verdict, 20, yPosition);
  
  yPosition += 20;

  // Score Breakdown Table
  doc.setFontSize(16);
  doc.setFont('helvetica', 'bold');
  doc.setTextColor(0, 0, 0);
  doc.text('Score Breakdown', 20, yPosition);
  
  yPosition += 10;

  const tableData = Object.entries(atsData.factors).map(([key, factor]) => [
    formatFactorName(key),
    `${factor.score.toFixed(1)}/${factor.max}`,
    `${((factor.score / factor.max) * 100).toFixed(1)}%`
  ]);

  autoTable(doc, {
    startY: yPosition,
    head: [['Factor', 'Score', 'Percentage']],
    body: tableData,
    theme: 'striped',
    headStyles: { fillColor: [102, 126, 234], textColor: [255, 255, 255] },
    styles: { fontSize: 10 },
    margin: { left: 20, right: 20 }
  });

  yPosition = doc.lastAutoTable.finalY + 15;

  // Recommendations
  if (atsData.recommendations && atsData.recommendations.length > 0) {
    doc.setFontSize(16);
    doc.setFont('helvetica', 'bold');
    doc.text('Recommendations', 20, yPosition);
    
    yPosition += 10;
    
    atsData.recommendations.forEach((rec, idx) => {
      if (yPosition > pageHeight - 30) {
        doc.addPage();
        yPosition = 20;
      }
      
      doc.setFontSize(11);
      doc.setFont('helvetica', 'bold');
      doc.setTextColor(102, 126, 234);
      doc.text(`${rec.priority.toUpperCase()} - ${rec.category}`, 20, yPosition);
      
      yPosition += 6;
      doc.setFont('helvetica', 'normal');
      doc.setTextColor(0, 0, 0);
      doc.text(rec.message, 25, yPosition, { maxWidth: pageWidth - 45 });
      
      yPosition += 10;
    });
  }

  // Matching Skills
  if (atsData.factors.skills && atsData.factors.skills.details) {
    if (yPosition > pageHeight - 40) {
      doc.addPage();
      yPosition = 20;
    }
    
    doc.setFontSize(16);
    doc.setFont('helvetica', 'bold');
    doc.text('Skills Analysis', 20, yPosition);
    
    yPosition += 10;
    doc.setFontSize(11);
    doc.setFont('helvetica', 'normal');
    doc.text(`Total Skills: ${atsData.factors.skills.details.count}`, 20, yPosition);
    doc.text(`Optimal Range: ${atsData.factors.skills.details.optimal_range}`, 20, yPosition + 6);
  }

  // Footer
  const totalPages = doc.internal.pages.length - 1;
  for (let i = 1; i <= totalPages; i++) {
    doc.setPage(i);
    doc.setFontSize(10);
    doc.setTextColor(150, 150, 150);
    doc.text(
      `Page ${i} of ${totalPages}`,
      pageWidth / 2,
      pageHeight - 10,
      { align: 'center' }
    );
  }

  // Save PDF
  const fileName = `ATS_Report_${resumeName.replace(/\s+/g, '_')}_${Date.now()}.pdf`;
  doc.save(fileName);
};

function getVerdictText(score) {
  if (score >= 85) {
    return 'Excellent: Your resume is highly optimized for ATS systems.';
  } else if (score >= 70) {
    return 'Good: Your resume is well-optimized with minor improvements needed.';
  } else if (score >= 50) {
    return 'Average: Your resume needs optimization to improve ATS compatibility.';
  } else {
    return 'Poor: Significant improvements needed for ATS compatibility.';
  }
}

function formatFactorName(name) {
  return name
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}



