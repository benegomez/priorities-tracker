# SQLAlchemy Mapping

## Project

class Project(Base):
    __tablename__ = 'projects'

    id = mapped_column(UUID)
    organization_id = mapped_column(UUID)
    name = mapped_column(String(200))

## ProjectPhase

class ProjectPhase(Base):
    __tablename__ = 'project_phases'

    project_id = mapped_column(ForeignKey('projects.id'))

## Relaciones

Project 1:N ProjectPhase
ProjectPhase 1:N Priority
Priority 1:N Task
