import React from 'react';

export const Alert = ({ variant, children }) => (
  <div className={`alert alert-${variant}`}>
    {children}
  </div>
);

export const AlertDescription = ({ children }) => (
  <div className="alert-description">
    {children}
  </div>
);