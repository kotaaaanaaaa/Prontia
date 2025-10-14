import Box from "@mui/material/Box";
import type * as React from "react";

const MainContents: React.FC<{ open: boolean }> = ({ open }) => {
  return (
    <Box className="main-contents">
      <p>Main Contents</p>
    </Box>
  );
};

export default MainContents;
