import ContentCopyIcon from "@mui/icons-material/ContentCopy";
import ThumbDownIcon from "@mui/icons-material/ThumbDownOutlined";
import ThumbUpIcon from "@mui/icons-material/ThumbUpOutlined";
import IconButton from "@mui/material/IconButton";
import Stack from "@mui/material/Stack";

const ChatResponseMenu: React.FC = () => {
  return (
    <Stack direction="row">
      <IconButton>
        <ContentCopyIcon />
      </IconButton>
      <IconButton>
        <ThumbUpIcon />
      </IconButton>
      <IconButton>
        <ThumbDownIcon />
      </IconButton>
    </Stack>
  );
};

export default ChatResponseMenu;
