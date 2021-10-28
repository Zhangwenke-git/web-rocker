"""
root
113bfdbc6e861ac97c732a5788804e1ab3
"""

import jenkins


class JenkinsUtils(object):

    def __init__(self, url, username, password):
        self._url = url
        self._username = username
        self._password = password

    def get_server_instance(self):
        server = jenkins.Jenkins(self._url, username=self._username, password=self._password)
        user = server.get_whoami()
        return server

    def get_version(self):
        return self.get_server_instance().get_version()

    def get_jobs(self):
        return {
            "jobs_count": self.get_server_instance().jobs_count(),
            "get_jobs": self.get_server_instance().get_jobs()}

    def create_job(self, job_name):
        return self.get_server_instance().create_job(job_name, config_xml=None)

    def get_job_config(self, job_name):
        return self.get_server_instance().get_job_config(job_name)

    def copy_job(self, job_name, new_job_name):
        return self.get_server_instance().copy_job(job_name, new_job_name)

    def build_job(self, job_name, parameters=None):
        return self.get_server_instance().build_job(job_name, parameters=parameters)

    def delete_build(self, job_name, number):
        return self.get_server_instance().delete_build(job_name, number)

    def get_job_info(self, job_name):
        return self.get_server_instance().get_job_info(job_name)['lastCompletedBuild']['number']

    def get_build_info(self, job_name, number):
        return self.get_server_instance().get_build_info(job_name, number)

    def get_build_console_output(self, job_name, number):
        return self.get_server_instance().get_build_console_output(job_name, number)

    def create_view(self, view_name):
        return self.get_server_instance().create_view(view_name, config_xml=jenkins.EMPTY_VIEW_CONFIG_XML)

    def get_views(self):
        return self.get_server_instance().get_views()



if __name__ == "__main__":
    url = "http://127.0.0.1:8080/"
    username = 'root'
    password="113bfdbc6e861ac97c732a5788804e1ab3"
    obj = JenkinsUtils(url,username,password)
    obj.build_job("BearFrameworkExecution",parameters={"testsuite":"test_ODM","testclass":"TestCase_ODM","testcase":"test_order_submit"})