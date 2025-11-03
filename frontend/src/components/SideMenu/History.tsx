import List from "@mui/material/List";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemText from "@mui/material/ListItemText";
import { ThemeProvider } from "@mui/material/styles";
import * as React from "react";
import { Link } from "react-router";
import { fetchHistory } from "../../api/chat";
import type { ConversationResponse } from "../../api/dto";
import { HistoryTheme } from "./HistoryTheme";

const histories: ConversationResponse[] = await fetchHistory();
const History: React.FC = () => {
  const [history, setHistory] =
    React.useState<ConversationResponse[]>(histories);
  return (
    <div className="history">
      <ThemeProvider theme={HistoryTheme}>
        <List>
          {history.map((item) => (
            <ListItemButton
              key={item.id}
              component={Link}
              to={`/chat/${item.id}`}
            >
              <ListItemText primary={item.title} />
            </ListItemButton>
          ))}
        </List>
      </ThemeProvider>
    </div>
  );
};

export default History;
