"use client";

import React, { useState, useEffect } from 'react';
import { Container, TextField, Button, Typography, Input, Box } from '@mui/material';

export default function Home() {
  const [coinData, setCoinData] = useState({});
  const [tradingCode, setTradingCode] = useState("");
  const [analysisResult, setAnalysisResult] = useState("");

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      // setFile(event.target.files[0]);
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
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom align="center">
        Trading Code Analyzer
      </Typography>
      <Box sx={{ mb: 2 }}>
        <TextField
          label="TradingView Code"
          multiline
          rows={4}
          variant="outlined"
          fullWidth
          margin="normal"
          value={tradingCode}
          onChange={(e) => setTradingCode(e.target.value)}
        />
      </Box>
      <Box sx={{ mb: 2 }}>
        <Input type="file" onChange={handleFileChange} fullWidth />
      </Box>
      <Box sx={{ textAlign: 'center' }}>
        <Button variant="contained" color="primary" size="large" onClick={handleSubmit}>Submit</Button>
      </Box>
      <Box sx={{ mt: 4 }}>
        <Typography variant="h6">Real-time Coin Data:</Typography>
        <pre>{JSON.stringify(coinData, null, 2)}</pre>
      </Box>
      <Box sx={{ mt: 4 }}>
        <Typography variant="h6">Analysis Result:</Typography>
        <pre>{analysisResult}</pre>
      </Box>
    </Container>
  );
}
