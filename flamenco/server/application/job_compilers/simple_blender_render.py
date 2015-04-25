import os
import json
import logging

class job_compiler():
    @staticmethod
    def compile(job, project, create_task):
        job_settings = json.loads(job.settings)
        task_type='simple_blender_render'
        parser='blender_render'

        task_settings={}
        task_settings['filepath'] = job_settings['filepath']
        task_settings['render_settings'] = job_settings['render_settings']
        task_settings['format'] = job_settings['format']
        task_settings['command_name'] = job_settings['command_name']

        #project = Project.query.filter_by(id = job.project_id).first()
        #filepath = task_settings['filepath']

        """task_settings['file_path_linux'] = os.path.join(project.path_linux, filepath)
        task_settings['file_path_win'] = os.path.join(project.path_win, filepath)
        task_settings['file_path_osx'] = os.path.join(project.path_osx, filepath)"""
        task_settings['file_path_linux'] = ""
        task_settings['file_path_win'] = ""
        task_settings['file_path_osx'] = ""
        #task_settings['settings'] = task.settings
        """task_settings['output_path_linux'] = os.path.join(project.render_path_linux, str(job.id), '#####')
        task_settings['output_path_win'] = os.path.join(project.render_path_win, str(job.id), '#####')
        task_settings['output_path_osx'] = os.path.join(project.render_path_osx, str(job.id), '#####')"""
        task_settings['output_path_linux'] = '#####'
        task_settings['output_path_win'] = '#####'
        task_settings['output_path_osx'] = '#####'
        task_settings['priority'] = job.priority
        task_settings['render_extras'] = job_settings['render_extras']

        #Chunk Generation
        job_frames_count = job_settings['frame_end'] - job_settings['frame_start'] + 1
        job_chunks_remainder = job_frames_count % job_settings['chunk_size']
        job_chunks_division = job_frames_count / job_settings['chunk_size']

        if job_chunks_remainder == 0:
            logging.debug('We have exact chunks')

            total_chunks = job_chunks_division
            task_settings['frame_start'] = job_settings['frame_start']
            task_settings['frame_end'] = job_settings['frame_start'] + job_settings['chunk_size'] - 1

            for chunk in range(total_chunks):
                logging.debug('Making chunk for job {0}'.format(job.id))

                name="{0}-{1}".format(task_settings['frame_start'], task_settings['frame_end'])
                create_task(job.id, task_type, task_settings, name, None, parser)

                task_settings['frame_start'] = task_settings['frame_end'] + 1
                task_settings['frame_end'] = task_settings['frame_start'] + job_settings['chunk_size'] - 1

        elif job_chunks_remainder == job_settings['chunk_size']:
            logging.debug('We have only 1 chunk')

            name="{0}-{1}".format(task_settings['frame_start'], task_settings['frame_end'])
            create_task(job.id, task_type, task_settings, name, None, parser)

        #elif job_chunks_remainder > 0 and \
        #     job_chunks_remainder < job_settings['chunk_size']:
        else:
            logging.debug('job_chunks_remainder : {0}'.format(job_chunks_remainder))
            logging.debug('job_frames_count     : {0}'.format(job_frames_count))
            logging.debug('job_chunks_division  : {0}'.format(job_chunks_division))

            total_chunks = job_chunks_division + 1
            task_settings['frame_start'] = job_settings['frame_start']
            task_settings['frame_end'] = job_settings['frame_start'] + job_settings['chunk_size'] - 1

            for chunk in range(total_chunks - 1):
                logging.debug('Making chunk for job {0}'.format(job.id))

                name="{0}-{1}".format(task_settings['frame_start'], task_settings['frame_end'])
                create_task(job.id, task_type, task_settings, name, None, parser)

                task_settings['frame_start'] = task_settings['frame_end'] + 1
                task_settings['frame_end'] = task_settings['frame_start'] + job_settings['chunk_size'] - 1

            task_settings['frame_end'] = task_settings['frame_start'] + job_chunks_remainder - 1
            name="{0}-{1}".format(task_settings['frame_start'], task_settings['frame_end'])

            create_task(job.id, task_type, task_settings, name, None, parser)
