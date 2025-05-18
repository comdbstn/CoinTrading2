import React, { useState, useEffect } from 'react';
import { Container, TextField, Button, Typography, Input, Box } from '@mui/material';

export default function Home() {
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  useEffect(() => {
    const script = document.createElement('script');
    script.src = 'https://s3.tradingview.com/tv.js';
    script.async = true;
    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    };
  }, []);

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom align="center">
        Trading Code Analyzer
      </Typography>
      <Box sx={{ mb: 2 }}>
        <TextField label="TradingView Code" multiline rows={4} variant="outlined" fullWidth margin="normal" />
      </Box>
      <Box sx={{ mb: 2 }}>
        <Input type="file" onChange={handleFileChange} fullWidth />
      </Box>
      <Box sx={{ textAlign: 'center' }}>
        <Button variant="contained" color="primary" size="large">Submit</Button>
      </Box>
      <Box sx={{ mt: 4 }}>
        <div id="tradingview-widget"></div>
      </Box>
    </Container>
  );
} 