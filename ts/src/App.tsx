import { useEffect, useState } from "react";
import axios from "axios";
import {
  BrowserRouter,
  Routes,
  Route,
  Link,
  useParams,
} from "react-router-dom";
import { format } from "date-fns";
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Card,
  CardContent,
  CircularProgress,
  Box,
  IconButton,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  Breadcrumbs,
} from "@mui/material";
import SmartDisplayIcon from "@mui/icons-material/SmartDisplay";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import InfoIcon from "@mui/icons-material/Info";
import HomeIcon from "@mui/icons-material/Home";

interface Channel {
  id: number;
  name: string;
}

interface Episode {
  id: number;
  name: string;
  season: number;
  number: number;
  number_overall: number;
  air_date: string | null;
  channels?: Channel[];
}

interface TvShow {
  id: number;
  name: string;
  created_at: string;
  updated_at: string | null;
  episodes?: Episode[];
}

const API_URL = "http://localhost:8010";

function EpisodeDetail() {
  const { id } = useParams<{ id: string }>();
  const [episode, setEpisode] = useState<Episode | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios
      .get<Episode>(`${API_URL}/episode`, { params: { episode_id: id } })
      .then((res) => setEpisode(res.data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <CircularProgress />;
  if (!episode) return <Typography>Episode not found</Typography>;

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {episode.name}
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        Season {episode.season} | Episode {episode.number} (Overall:{" "}
        {episode.number_overall})
      </Typography>

      <Card sx={{ mt: 3, mb: 3 }}>
        <CardContent>
          <Typography variant="h6">Air Date</Typography>
          <Typography gutterBottom>
            {episode.air_date
              ? format(new Date(episode.air_date), "PPPP")
              : "Unknown"}
          </Typography>

          <Typography variant="h6" sx={{ mt: 2 }}>
            Airing on Channels
          </Typography>
          <Box sx={{ display: "flex", gap: 1, flexWrap: "wrap", mt: 1 }}>
            {episode.channels && episode.channels.length > 0 ? (
              episode.channels.map((channel) => (
                <Chip
                  key={channel.id}
                  label={channel.name}
                  color="primary"
                  variant="outlined"
                />
              ))
            ) : (
              <Typography variant="body2" color="text.secondary">
                No channel information available.
              </Typography>
            )}
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
}

function TvShowDetail() {
  const { id } = useParams<{ id: string }>();
  const [show, setShow] = useState<TvShow | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios
      .get<TvShow>(`${API_URL}/tvshow`, { params: { tvshow_id: id } })
      .then((res) => setShow(res.data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <CircularProgress />;
  if (!show) return <Typography>TV Show not found</Typography>;

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {show.name}
      </Typography>
      <Typography variant="body2" color="text.secondary" gutterBottom>
        Last Updated:{" "}
        {show.updated_at ? format(new Date(show.updated_at), "PPpp") : "Never"}
      </Typography>

      <Typography variant="h5" sx={{ mt: 4, mb: 2 }}>
        Episodes
      </Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Season</TableCell>
              <TableCell>Number</TableCell>
              <TableCell>Overall</TableCell>
              <TableCell>Name</TableCell>
              <TableCell align="right">Details</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {show.episodes?.map((ep) => (
              <TableRow key={ep.id}>
                <TableCell>{ep.season}</TableCell>
                <TableCell>{ep.number}</TableCell>
                <TableCell>{ep.number_overall}</TableCell>
                <TableCell>{ep.name}</TableCell>
                <TableCell align="right">
                  <IconButton
                    component={Link}
                    to={`/episodes/${ep.id}`}
                    color="primary"
                  >
                    <InfoIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}

function TvShowList() {
  const [shows, setShows] = useState<TvShow[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios
      .get<TvShow[]>(`${API_URL}/tvshows`)
      .then((res) => setShows(res.data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <CircularProgress />;

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        TV Shows Library
      </Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Created At</TableCell>
              <TableCell>Updated At</TableCell>
              <TableCell align="right">View</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {shows.map((row) => (
              <TableRow key={row.id} hover>
                <TableCell
                  component="th"
                  scope="row"
                  sx={{ fontWeight: "bold" }}
                >
                  {row.name}
                </TableCell>
                <TableCell>
                  {row.created_at
                    ? format(new Date(row.created_at), "PP")
                    : "-"}
                </TableCell>
                <TableCell>
                  {row.updated_at
                    ? format(new Date(row.updated_at), "PP")
                    : "-"}
                </TableCell>
                <TableCell align="right">
                  <IconButton
                    component={Link}
                    to={`/tvshows/${row.id}`}
                    color="primary"
                    aria-label="view details"
                  >
                    <ArrowForwardIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Box sx={{ flexGrow: 1, bgcolor: "#f5f5f5", minHeight: "100vh" }}>
        <AppBar position="static">
          <Toolbar>
            <SmartDisplayIcon sx={{ mr: 2 }} />
            <Typography
              variant="h6"
              component={Link}
              to="/"
              sx={{ flexGrow: 1, textDecoration: "none", color: "inherit" }}
            >
              TV Show Manager
            </Typography>
          </Toolbar>
        </AppBar>

        <Container sx={{ py: 4 }} maxWidth={false}>
          <Box mb={2}>
            <Breadcrumbs aria-label="breadcrumb">
              <Link
                to="/"
                style={{
                  display: "flex",
                  alignItems: "center",
                  textDecoration: "none",
                  color: "inherit",
                }}
              >
                <HomeIcon sx={{ mr: 0.5 }} fontSize="inherit" />
                Home
              </Link>
            </Breadcrumbs>
          </Box>

          <Routes>
            <Route path="/" element={<TvShowList />} />
            <Route path="/tvshows/:id" element={<TvShowDetail />} />
            <Route path="/episodes/:id" element={<EpisodeDetail />} />
          </Routes>
        </Container>
      </Box>
    </BrowserRouter>
  );
}

export default App;
