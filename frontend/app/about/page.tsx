// app/about/page.tsx
'use client';

import React from 'react';
import { Box, Typography, Container, Paper } from '@mui/material';

const AboutPage: React.FC = () => {
  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          About Us
        </Typography>
        <Typography variant="body1" paragraph>
          Welcome to our website! We are passionate about delivering quality content and services to our users.
        </Typography>

        <Box sx={{ mt: 4 }}>
          <Typography variant="h5" component="h2" gutterBottom>
            Our Mission
          </Typography>
          <Typography variant="body1" paragraph>
            Our mission is to empower individuals and businesses with the tools and knowledge they need to succeed.
          </Typography>
        </Box>

        <Box sx={{ mt: 4 }}>
          <Typography variant="h5" component="h2" gutterBottom>
            Our Team
          </Typography>
          <Typography variant="body1">
            We are a team of dedicated professionals with expertise in various fields. Together, we strive to create meaningful impact.
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
};

export default AboutPage;
