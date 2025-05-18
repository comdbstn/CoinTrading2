"use client";

import React, { useState, useEffect } from 'react';
import { Container, TextField, Button, Typography, Input, Box } from '@mui/material';

export default function Home() {
  const [coinData, setCoinData] = useState({});
  const [tradingCode, setTradingCode] = useState("");
  const [analysisResult, setAnalysisResult] = useState("");

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      const file = event.target.files[0];
      console.log('Selected file:', file);
    }
  };

  useEffect(() => {
    const fetchCoinData = async () => {
      try {
        const response = await fetch('/api/coin-data/');
        const data = await response.json();
        setCoinData(data);
      } catch (error) {
        console.error('Error fetching coin data:', error);
      }
    };
    fetchCoinData();
  }, []);

  const handleSubmit = async () => {
    try {
      const response = await fetch('/api/submit-code/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code: tradingCode }),
      });
      const data = await response.json();
      setAnalysisResult(data.optimized_code);
    } catch (error) {
      console.error('Error submitting code:', error);
    }
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4, bgcolor: 'white', color: 'black', p: 3, borderRadius: 2, boxShadow: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom align="center" sx={{ fontWeight: 'bold', mb: 3 }}>
        Trading Code Analyzer
      </Typography>
      <Box sx={{ mb: 3 }}>
        <TextField
          label="TradingView Code"
          multiline
          rows={6}
          variant="outlined"
          fullWidth
          margin="normal"
          value={tradingCode}
          onChange={(e) => setTradingCode(e.target.value)}
          sx={{ bgcolor: 'white', borderRadius: 1 }}
        />
      </Box>
      <Box sx={{ mb: 3 }}>
        <Input type="file" onChange={handleFileChange} fullWidth sx={{ bgcolor: 'white', p: 1, borderRadius: 1 }} />
      </Box>
      <Box sx={{ textAlign: 'center', mb: 3 }}>
        <Button variant="contained" color="primary" size="large" onClick={handleSubmit} sx={{ fontWeight: 'bold' }}>Submit</Button>
      </Box>
      <Box sx={{ mt: 4 }}>
        <Typography variant="h6" sx={{ fontWeight: 'bold' }}>Real-time Coin Data:</Typography>
        <pre>{JSON.stringify(coinData, null, 2)}</pre>
      </Box>
      <Box sx={{ mt: 4 }}>
        <Typography variant="h6" sx={{ fontWeight: 'bold' }}>Analysis Result:</Typography>
        <pre>{analysisResult}</pre>
      </Box>
    </Container>
  );
}
