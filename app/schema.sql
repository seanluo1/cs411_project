DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Likes;
DROP TABLE IF EXISTS Song;
DROP TABLE IF EXISTS Created;
DROP TABLE IF EXISTS Follows;
DROP TABLE IF EXISTS Remix;
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Remixed;
DROP TABLE IF EXISTS PushNotification;

CREATE TABLE User (
  Id INTEGER PRIMARY KEY AUTOINCREMENT,
  FirstName TEXT NOT NULL,
  LastName TEXT NOT NULL,
  Email TEXT UNIQUE NOT NULL,
  Password TEXT NOT NULL,
  SongOfWeek TEXT NOT NULL
);

CREATE TABLE Song (
  SongId INTEGER PRIMARY KEY AUTOINCREMENT,
  SongName TEXT NOT NULL,
  Genre TEXT NOT NULL,
  Song_Url TEXT NOT NULL
);

CREATE TABLE PushNotification (
  NotificationId INTEGER PRIMARY KEY AUTOINCREMENT,
  UserId TEXT NOT NULL,
  MessageText TEXT NOT NULL,
  Song_Url TEXT NOT NULL
);

CREATE TABLE Remix (
  RemixId INTEGER PRIMARY KEY AUTOINCREMENT,
  RemixName TEXT NOT NULL,
  RemixLink TEXT NOT NULL
);

CREATE TABLE Artist (
  ArtistId INTEGER PRIMARY KEY AUTOINCREMENT,
  ArtistName TEXT NOT NULL
);

CREATE TABLE Created (
  ArtistId INTEGER NOT NULL,
  SongId INTEGER NOT NULL,
  PRIMARY KEY(ArtistId, SongId),
  FOREIGN KEY (ArtistId) REFERENCES User(Id),
  FOREIGN KEY (SongId) REFERENCES Song(Id)
);

CREATE TABLE Follows (
  FollowerId INTEGER NOT NULL,
  FolloweeId INTEGER NOT NULL,
  PRIMARY KEY(FollowerId, FolloweeId),
  FOREIGN KEY (FollowerId) REFERENCES User(Id),
  FOREIGN KEY (FolloweeId) REFERENCES User(Id)
);

CREATE TABLE Likes (
  UserId INTEGER NOT NULL,
  SongId INTEGER NOT NULL,
  PRIMARY KEY(UserId, SongId),
  FOREIGN KEY (UserId) REFERENCES User(Id),
  FOREIGN KEY (SongId) REFERENCES Song(Id)
);

CREATE TABLE Remixed (
  RemixId INTEGER NOT NULL,
  SongId INTEGER NOT NULL,
  ArtistId INTEGER NOT NULL,
  PRIMARY KEY(RemixId, ArtistId),
  FOREIGN KEY (RemixId) REFERENCES Remix(Id),
  FOREIGN KEY (SongId) REFERENCES Song(Id),
  FOREIGN KEY (ArtistId) REFERENCES Artist(Id)
);
