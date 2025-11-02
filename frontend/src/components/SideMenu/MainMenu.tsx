import EditSquareIcon from "@mui/icons-material/EditSquare";
import SearchIcon from "@mui/icons-material/Search";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import type { OverridableComponent } from "@mui/material/OverridableComponent";
import Stack from "@mui/material/Stack";
import type { SvgIconTypeMap } from "@mui/material/SvgIcon";

type SvgIconComponent = OverridableComponent<SvgIconTypeMap<{}, "svg">>;

const MenuButtonItem: React.FC<{
  expand: boolean;
  Icon: SvgIconComponent;
  text: string;
}> = ({ expand, Icon, text }) => {
  return (
    <>
      {expand ? (
        <Button startIcon={<Icon />}>{text}</Button>
      ) : (
        <IconButton>{<Icon />}</IconButton>
      )}
    </>
  );
};

const MainMenu: React.FC<{ expand: boolean }> = ({ expand }) => {
  return (
    <div className="main-menu">
      <Stack direction="column">
        <MenuButtonItem expand={expand} Icon={EditSquareIcon} text="Edit" />
        <MenuButtonItem expand={expand} Icon={SearchIcon} text="Search" />
      </Stack>
    </div>
  );
};

export default MainMenu;
