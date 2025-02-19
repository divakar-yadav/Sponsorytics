import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './UploadSection.css';
function UploadSection() {
  const [file1, setFile1] = useState(null);
  const [file2, setFile2] = useState(null);
  const navigate = useNavigate();

  const handleFileChange1 = (e) => {
    setFile1(e.target.files[0]);
  };

  const handleFileChange2 = (e) => {
    setFile2(e.target.files[0]);
  };

  const handleGenerateDashboard = () => {
    if (file1 && file2) {
      navigate('/dashboard');
    } else {
      alert('Please upload both files before generating the dashboard.');
    }
  };

  return (
    <div className='upload-container' style={{ textAlign: 'center' }}>
        <div className='upload-section'>
                <h2>Upload Files</h2>
                <div className='file-upload'>
                        <div className='file-upload-1'>
                        <input type="file" onChange={handleFileChange1} />
                    </div>
                    <div className='file-upload-2'>
                        <input type="file" onChange={handleFileChange2} />
                    </div>
                    <button className='recommendation-button' onClick={handleGenerateDashboard} style={{  padding: '10px', cursor: 'pointer', width: '40%', margin: 'auto', marginTop: '20px' }}>
                        Generate Recommendation Dashboard
                    </button>
                </div>
        </div>
    </div>
  );
}

export default UploadSection;
